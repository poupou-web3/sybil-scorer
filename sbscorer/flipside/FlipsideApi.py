import os

import numpy as np
import pandas as pd
from shroomdk import ShroomDK


def save_csv(df, path_to_export, csv_file):
    if not os.path.exists(path_to_export):
        os.makedirs(path_to_export)
    df.to_csv(csv_file, index=False)


class FlipsideApi(object):

    def __init__(self, api_key, page_size=100000, timeout_minutes=4, page_number=1, max_address=100):
        self.api_key = api_key

        # Initialize `ShroomDK`
        self.sdk = ShroomDK(api_key)
        # return up to 100,000 results per GET request on the query id
        self.PAGE_SIZE = page_size
        # timeout in minutes
        self.TIMEOUT_MINUTES = timeout_minutes
        # return results of page 1
        self.PAGE_NUMBER = page_number
        # max address to query
        self.MAX_ADDRESS = max_address

    def execute_query(self, sql):
        try:
            query_result_set = self.sdk.query(sql,
                                              page_size=self.PAGE_SIZE,
                                              timeout_minutes=self.TIMEOUT_MINUTES)
        except Exception as e:
            print(e)
            print(sql)
            return pd.DataFrame()  # return empty dataframe
        return pd.DataFrame(query_result_set.records)

    def extract_transactions(self, extract_dir, df_address):
        list_network = ["ethereum", "polygon",
                        "arbitrum", "avalanche", "gnosis", "optimism"]
        for network in list_network:
            self.extract_transactions_net(extract_dir, df_address, network)

    def extract_transactions_net(self, extract_dir, df_address, network):
        print("Extracting transactions for network: ", network)
        len_address = len(df_address)
        q, r = divmod(len_address, self.MAX_ADDRESS)
        if r != 0:
            q += 1
        for i in range(q):
            start_index = i * self.MAX_ADDRESS
            end_index = (i + 1) * self.MAX_ADDRESS
            print(
                f"Extracting transactions for address: {start_index} - {end_index}")
            df = self.get_transactions(
                df_address[start_index: end_index], network)
            if df.shape[0] == 0:
                self.extract_transactions_rec(
                    df_address, start_index, end_index, network, extract_dir)
            else:
                self.export_address(
                    df, df_address[start_index: end_index], extract_dir, network)

    def get_transactions(self, df_address, network):
        if network == "ethereum":
            sql = self.get_eth_transactions_sql_query(df_address)
        elif network == "polygon":
            sql = self.get_polygon_transactions_sql_query(df_address)
        elif network == "arbitrum":
            sql = self.get_arbitrum_transactions_sql_query(df_address)
        elif network == "avalanche":
            sql = self.get_avalanche_transactions_sql_query(df_address)
        elif network == "gnosis":
            sql = self.get_gnosis_transactions_sql_query(df_address)
        elif network == "optimism":
            sql = self.get_optimism_transactions_sql_query(df_address)
        else:
            raise Exception("Network not supported")

        df = self.execute_query(sql)
        return df

    @staticmethod
    def export_address(df, np_address, extract_dir, network):
        """
        Export the dataframe to a csv file

        Change the idea and exporting straight to an account based csv for easier csv manipulation from other tools
        If there is no transactions them the file is not created, creating empty file is useless.
        Parameters
        ----------
        df : pd.DataFrame
            Dataframe containing the transactions of potentially many addresses
        np_address : numpy.ndarray
            Array containing the addresses
        extract_dir : str
            Directory where to export the csv file
        network : str
            Network of the transactions

        Returns
        -------

        """
        for address in np_address:
            df_address_transactions = df[np.logical_or(
                df.from_address == address, df.to_address == address)]
            path_to_export = os.path.join(extract_dir, network)
            csv_file = os.path.join(path_to_export, f"{address}_tx.csv")
            if df_address_transactions.shape[0] > 0:
                save_csv(df_address_transactions, path_to_export, csv_file)
            else:
                print(f"No transactions found for address {address}")

    def extract_transactions_rec(self, df_address, start_index, end_index, network, extract_dir):
        end_first_slice = (start_index + end_index) // 2
        print("Retrying with smaller query")
        self.extract_transactions_between_rec(
            df_address, start_index, end_first_slice, network, extract_dir)
        self.extract_transactions_between_rec(
            df_address, end_first_slice, end_index, network, extract_dir)

    def extract_transactions_between_rec(self, df_address, start_index, end_index, network, extract_dir):
        print(
            f"Extracting transactions for address: {start_index} - {end_index}")
        df = self.get_transactions(df_address[start_index: end_index], network)
        if df.shape[0] == 0:
            # recursive call
            print("Retrying with smaller query")
            self.extract_transactions_rec(
                df_address, start_index, end_index, network, extract_dir)
        else:
            self.export_address(
                df, df_address[start_index: end_index], extract_dir, network)

    @staticmethod
    def get_string_address(df_address):
        lower_str = ""
        for add in df_address:
            lower_str += f'LOWER(\'{add}\'),'
        lower_str = lower_str[:-1]
        return lower_str

    def get_eth_transactions_sql_query(self, df_address, limit=0):
        address_list = self.get_string_address(df_address)
        if limit != 0:
            string_limit = f"LIMIT {limit}"
        else:
            string_limit = ""
        sql = f"""
                SELECT TX_HASH,
                BLOCK_TIMESTAMP,
                FROM_ADDRESS,
                TO_ADDRESS,
                GAS_LIMIT,
                GAS_USED,
                TX_FEE,
                ETH_VALUE
                FROM ethereum.core.fact_transactions
                WHERE FROM_ADDRESS IN ({address_list})
                OR TO_ADDRESS IN ({address_list})
                {string_limit};
                """
        return sql

    def get_polygon_transactions_sql_query(self, df_address, limit=0):
        address_list = self.get_string_address(df_address)
        if limit != 0:
            string_limit = f"LIMIT {limit}"
        else:
            string_limit = ""
        sql = f"""
                SELECT TX_HASH,
                BLOCK_TIMESTAMP,
                FROM_ADDRESS,
                TO_ADDRESS,
                GAS_LIMIT,
                GAS_USED,
                TX_FEE,
                MATIC_VALUE
                FROM polygon.core.fact_transactions
                WHERE FROM_ADDRESS IN ({address_list})
                OR TO_ADDRESS IN ({address_list})
                {string_limit};
                """
        return sql

    def get_arbitrum_transactions_sql_query(self, df_address, limit=0):
        address_list = self.get_string_address(df_address)
        if limit != 0:
            string_limit = f"LIMIT {limit}"
        else:
            string_limit = ""
        sql = f"""
                SELECT TX_HASH,
                BLOCK_TIMESTAMP,
                FROM_ADDRESS,
                TO_ADDRESS,
                GAS_LIMIT,
                GAS_USED,
                TX_FEE,
                ETH_VALUE
                FROM arbitrum.core.fact_transactions
                WHERE FROM_ADDRESS IN ({address_list})
                OR TO_ADDRESS IN ({address_list})
                {string_limit};
                """
        return sql

    def get_avalanche_transactions_sql_query(self, df_address, limit=0):
        address_list = self.get_string_address(df_address)
        if limit != 0:
            string_limit = f"LIMIT {limit}"
        else:
            string_limit = ""
        sql = f"""
                SELECT TX_HASH,
                BLOCK_TIMESTAMP,
                FROM_ADDRESS,
                TO_ADDRESS,
                GAS_LIMIT,
                GAS_USED,
                TX_FEE,
                AVAX_VALUE
                FROM avalanche.core.fact_transactions
                WHERE FROM_ADDRESS IN ({address_list})
                OR TO_ADDRESS IN ({address_list})
                {string_limit};
                """
        return sql

    def get_gnosis_transactions_sql_query(self, df_address, limit=0):
        address_list = self.get_string_address(df_address)
        if limit != 0:
            string_limit = f"LIMIT {limit}"
        else:
            string_limit = ""
        sql = f"""
                    SELECT TX_HASH,
                    BLOCK_TIMESTAMP,
                    FROM_ADDRESS,
                    TO_ADDRESS,
                    GAS_LIMIT,
                    GAS_USED,
                    TX_FEE
                    FROM gnosis.core.fact_transactions
                    WHERE FROM_ADDRESS IN ({address_list})
                    OR TO_ADDRESS IN ({address_list})
                    {string_limit};
                    """
        return sql

    def get_optimism_transactions_sql_query(self, df_address, limit=0):
        address_list = self.get_string_address(df_address)
        if limit != 0:
            string_limit = f"LIMIT {limit}"
        else:
            string_limit = ""
        sql = f"""
                    SELECT TX_HASH,
                    BLOCK_TIMESTAMP,
                    FROM_ADDRESS,
                    TO_ADDRESS,
                    GAS_LIMIT,
                    GAS_USED,
                    TX_FEE,
                    ETH_VALUE
                    FROM optimism.core.fact_transactions
                    WHERE FROM_ADDRESS IN ({address_list})
                    OR TO_ADDRESS IN ({address_list})
                    {string_limit};
                    """
        return sql

    def get_cross_chain_info_sql_query(self, df_address, info_type="label", limit=0):
        address_list = self.get_string_address(df_address)
        if info_type == "label":
            table_name = "crosschain.address_labels"
        elif info_type == "tag":
            table_name = "crosschain.address_tags"
        else:
            Exception("Invalid info type")
        if limit != 0:
            string_limit = f"LIMIT {limit}"
        else:
            string_limit = ""

        sql = f"""
                SELECT *
                FROM {table_name}
                WHERE ADDRESS IN ({address_list})
                {string_limit};
                """
        return sql

    @staticmethod
    def get_price_feed_eth_ftm_sql_query(limit=0):
        if limit != 0:
            string_limit = f"LIMIT {limit}"
        else:
            string_limit = ""
        sql = f"""
                SELECT ID,
                RECORDED_HOUR,
                "OPEN"	
                FROM crosschain.core.fact_hourly_prices
                where	ID in ('ethereum', 'fantom')
                AND RECORDED_HOUR > DATE(2023-12-11)
                ORDER BY RECORDED_HOUR DESC
                {string_limit};
                """
        return sql
