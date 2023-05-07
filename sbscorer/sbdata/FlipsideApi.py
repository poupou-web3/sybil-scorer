import os

import numpy as np
import pandas as pd
from flipside import Flipside


def save_csv(df, path_to_export, csv_file):
    if not os.path.exists(path_to_export):
        os.makedirs(path_to_export)
    df.to_csv(csv_file, index=False)


class FlipsideApi(object):
    """
    This class is used to query the flipside crypto api
    It has methods to easily retrieve the data and save it to csv
    """

    def __init__(self, api_key, max_age_minutes=30, ttl=30, timeout_minutes=5, retry_interval=1, page_size=100000,
                 page_number=1, max_address=100, cached=True):
        """
        Init method of FlipsideApi
        Parameters
        ----------
        api_key : str
            The api key to use to query flipside https://sdk.flipsidecrypto.xyz/shroomdk/apikeys
        max_age_minutes : int
            The max age in minutes of the query default is 30 because queries are also cached for 30 minutes
        page_size : int
            The number of rows to return per page default is 100000
        timeout_minutes : int
            The timeout in minutes default is 4
        page_number : int
            The page number to return default is 1
        max_address : int
            Max number of addresses to query default is 100
        ttl : int
            The time to live in minutes default is 60 minutes, ie the time the query is saved in the cache.
        cached : bool
            If the query should be cached default is True. If you query several page it will run faster
        retry_interval : int
            The retry interval in seconds default is 1
        """
        self.api_key = api_key

        # Initialize `FlipsideApi`
        self.sdk = Flipside(api_key)
        self.MAX_AGE_MINUTES = max_age_minutes
        # return up to 100,000 results per GET request on the query id
        self.PAGE_SIZE = page_size
        # timeout in minutes
        self.TIMEOUT_MINUTES = timeout_minutes
        # return results of page 1
        self.PAGE_NUMBER = page_number
        # max address to query.
        # It is not recommended to go above 10000 it already takes a long time and it depends on the network
        # You will probably have to run more queries because either the query times out or the max rows is reached
        # At 100 tx per address the 1 million rows is reached if you use max_address=10000
        # At 1000 tx per address the 1 million rows is reached if you use max_address=1000
        # on ethereum 1000 or 2000 should be fine but on polygon it is better to use 500
        self.MAX_ADDRESS = max_address
        # TTL for the query id in minutes
        self.TTL_MINUTES = ttl
        # Cached query id
        self.CACHED = cached
        # Retry interval in seconds
        self.RETRY_INTERVAL_SECONDS = retry_interval
        # The max output size of flipside
        self.MAX_ROWS = 1000000  # 1 million is the max output size of flipside

    def execute_query(self, sql):
        """
        Execute a query and return a pandas dataframe, it will automatically query all the pages using class parameters.
        Parameters
        ----------
        sql : str
            The sql query to execute

        Returns
        -------
        df : pandas dataframe
            The dataframe containing the results of the query

        """
        page_number = 1

        try:
            query_result_set = self.sdk.query(sql,
                                              max_age_minutes=self.MAX_AGE_MINUTES,
                                              page_size=self.PAGE_SIZE,
                                              page_number=page_number,
                                              timeout_minutes=self.TIMEOUT_MINUTES,
                                              ttl_minutes=self.TTL_MINUTES,
                                              cached=self.CACHED,
                                              retry_interval_seconds=self.RETRY_INTERVAL_SECONDS)

        except Exception as e:
            print(e)
            print(sql)
            return pd.DataFrame()  # return empty dataframe

        df = query_result_set.records
        df_size = df.shape[0]
        list_df = [df]
        while df_size == self.PAGE_SIZE:
            try:
                page_results = self.sdk.get_query_results(
                    query_result_set.query_id,
                    page_number=page_number,
                    page_size=self.PAGE_SIZE)
                df = pd.DataFrame(page_results.records)
                df_size = df.shape[0]

            except Exception as e:
                print(e)
                print(f'failed on page {page_number}')
                df_size = 0  # break the loop

            page_number += 1
            list_df.append(df)

        df = pd.concat(list_df)
        if df.shape[0] == self.MAX_ROWS:
            print("WARNING: the query is probably not returning all the results, you should decrease the max_address")
        return df

    def extract_transactions(self, extract_dir, array_address):
        """
        Extract the transactions contained in array_address for all the networks and save them to csv in the extract_dir

        Parameters
        ----------
        extract_dir : str
            The directory where to save the csv files
        array_address : array
            The array of addresses to extract

        Returns
        -------
        None
            Create csv files in the extract_dir

        """
        list_network = ["ethereum", "polygon",
                        "arbitrum", "avalanche", "gnosis", "optimism"]
        for network in list_network:
            self.extract_transactions_net(extract_dir, array_address, network)

    def extract_transactions_net(self, extract_dir, array_address, network):
        """
        Extract the transactions contained in array_address for the network and save them to csv in the extract_dir
        Each csv is named as eoa_tx.csv and is stored in a folder named after the network

        Parameters
        ----------
        extract_dir : str
            The directory where to save the csv files
        array_address : array
            The array of addresses to extract
        network : str
            The network to extract the transactions from

        Returns
        -------
        None
            Create csv files in the extract_dir

        """
        print("Extracting transactions for network: ", network)
        len_address = len(array_address)
        q, r = divmod(len_address, self.MAX_ADDRESS)
        if r != 0:
            q += 1
        for i in range(q):
            start_index = i * self.MAX_ADDRESS
            end_index = (i + 1) * self.MAX_ADDRESS
            print(
                f"Extracting transactions for address: {start_index} - {end_index}")
            df = self.get_transactions(
                array_address[start_index: end_index], network)
            if df.shape[0] == 0 or df.shape == self.MAX_ROWS:  # retry with smaller query timeout or max rows
                self.extract_transactions_rec(
                    array_address, start_index, end_index, network, extract_dir)
            else:
                self.export_address(
                    df, array_address[start_index: end_index], extract_dir, network)

    def get_transactions(self, array_address, network):
        """
        Get the transactions for the array of addresses and the network in a df

        Parameters
        ----------
        array_address : array
            The array of addresses to extract
        network :str
            The network to extract the transactions from

        Returns
        -------
        df : pandas dataframe
            The dataframe containing the transactions

        """
        if network == "ethereum":
            sql = self.get_eth_transactions_sql_query(array_address)
        elif network == "polygon":
            sql = self.get_polygon_transactions_sql_query(array_address)
        elif network == "arbitrum":
            sql = self.get_arbitrum_transactions_sql_query(array_address)
        elif network == "avalanche":
            sql = self.get_avalanche_transactions_sql_query(array_address)
        elif network == "gnosis":
            sql = self.get_gnosis_transactions_sql_query(array_address)
        elif network == "optimism":
            sql = self.get_optimism_transactions_sql_query(array_address)
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
        np_address = np.char.lower(np_address.astype(str))
        for address in np_address:
            df_address_transactions = df[np.logical_or(
                df.from_address == address, df.to_address == address)]
            path_to_export = os.path.join(extract_dir, network)
            csv_file = os.path.join(path_to_export, f"{address}_tx.csv")
            if df_address_transactions.shape[0] > 0:
                save_csv(df_address_transactions, path_to_export, csv_file)
            # else:
            #     print(f"No transactions found for address {address}")

    def extract_transactions_rec(self, array_address, start_index, end_index, network, extract_dir):
        """
        Recursive method to extract the transactions for the array of addresses and the network in a df
        It is used to retry with smaller query if the query timeout or the max rows are reached
        Parameters
        ----------
        array_address : array
            The array of addresses to extract
        start_index : int
            The start index of the array_address
        end_index : int
            The end index of the array_address
        network : str
            The network to extract the transactions from
        extract_dir : str
            The directory where to save the csv files

        Returns
        -------
        None

        """
        end_first_slice = (start_index + end_index) // 2
        print("Retrying with smaller query")
        self.extract_transactions_between_rec(
            array_address, start_index, end_first_slice, network, extract_dir)
        self.extract_transactions_between_rec(
            array_address, end_first_slice, end_index, network, extract_dir)

    def extract_transactions_between_rec(self, array_address, start_index, end_index, network, extract_dir):
        """
        Recursive method to extract the transactions for the array of addresses and the network in a df
        It is used to retry with smaller query if the query timeout or the max rows are reached
        Parameters
        ----------
        array_address : array
            The array of addresses to extract
        start_index : int
            The start index of the array_address
        end_index : int
            The end index of the array_address
        network : str
            The network to extract the transactions from
        extract_dir : str
            The directory where to save the csv files

        Returns
        -------
        None

        """
        print(
            f"Extracting transactions for address: {start_index} - {end_index}")
        df = self.get_transactions(array_address[start_index: end_index], network)
        if df.shape[0] == 0:
            # recursive call
            print("Retrying with smaller query")
            self.extract_transactions_rec(
                array_address, start_index, end_index, network, extract_dir)
        else:
            self.export_address(
                df, array_address[start_index: end_index], extract_dir, network)

    @staticmethod
    def get_string_address(array_address):
        """
        Get the string of the array of addresses to use in the sql query
        Parameters
        ----------
        array_address : array

        Returns
        -------
        lower_str : str
            The string to use in the sql query

        """
        lower_str = ""
        for add in array_address:
            lower_str += f'LOWER(\'{add}\'),'
        lower_str = lower_str[:-1]
        return lower_str

    def get_eth_transactions_sql_query(self, array_address, limit=0):
        """
        Get the sql query to extract the transactions for the array of addresses and ethereum network
        Parameters
        ----------
        array_address : array
            The array of addresses to extract
        limit : int
            The limit of the query default 0 everything is retrieved. The limit is the Keyword LIMIT in SQL.

        Returns
        -------
        sql : str
            The sql query to execute

        """
        str_list_add = self.get_string_address(array_address)
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
                WHERE FROM_ADDRESS IN ({str_list_add})
                OR TO_ADDRESS IN ({str_list_add})
                {string_limit};
                """
        return sql

    def get_polygon_transactions_sql_query(self, array_address, limit=0):
        """
        Get the sql query to extract the transactions for the array of addresses and polygon network
        Parameters
        ----------
        array_address : array
            The array of addresses to extract
        limit : int
            The limit of the query default 0 everything is retrieved. The limit is the Keyword LIMIT in SQL.

        Returns
        -------
        sql : str
            The sql query to execute

        """
        str_list_add = self.get_string_address(array_address)
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
                WHERE FROM_ADDRESS IN ({str_list_add})
                OR TO_ADDRESS IN ({str_list_add})
                {string_limit};
                """
        return sql

    def get_arbitrum_transactions_sql_query(self, array_address, limit=0):
        """
        Get the sql query to extract the transactions for the array of addresses and arbitrum network
        Parameters
        ----------
        array_address : array
            The array of addresses to extract
        limit : int
            The limit of the query default 0 everything is retrieved. The limit is the Keyword LIMIT in SQL.

        Returns
        -------
        sql : str
            The sql query to execute

        """
        str_list_add = self.get_string_address(array_address)
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
                WHERE FROM_ADDRESS IN ({str_list_add})
                OR TO_ADDRESS IN ({str_list_add})
                {string_limit};
                """
        return sql

    def get_avalanche_transactions_sql_query(self, array_address, limit=0):
        """
        Get the sql query to extract the transactions for the array of addresses and avalanche network
        Parameters
        ----------
        array_address : array
            The array of addresses to extract
        limit : int
            The limit of the query default 0 everything is retrieved. The limit is the Keyword LIMIT in SQL.

        Returns
        -------
        sql : str
            The sql query to execute
        """
        str_list_add = self.get_string_address(array_address)
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
                WHERE FROM_ADDRESS IN ({str_list_add})
                OR TO_ADDRESS IN ({str_list_add})
                {string_limit};
                """
        return sql

    def get_gnosis_transactions_sql_query(self, array_address, limit=0):
        """
        Get the sql query to extract the transactions for the array of addresses and gnosis network
        Parameters
        ----------
        array_address : array
            The array of addresses to extract
        limit : int
            The limit of the query default 0 everything is retrieved. The limit is the Keyword LIMIT in SQL.

        Returns
        -------
        sql : str
            The sql query to execute

        """
        str_list_add = self.get_string_address(array_address)
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
                    WHERE FROM_ADDRESS IN ({str_list_add})
                    OR TO_ADDRESS IN ({str_list_add})
                    {string_limit};
                    """
        return sql

    def get_optimism_transactions_sql_query(self, array_address, limit=0):
        """
        Get the sql query to extract the transactions for the array of addresses and optimism network
        Parameters
        ----------
        array_address : array
            The array of addresses to extract
        limit : int
            The limit of the query default 0 everything is retrieved. The limit is the Keyword LIMIT in SQL.

        Returns
        -------
        sql : str
            The sql query to execute

        """
        str_list_add = self.get_string_address(array_address)
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
                    WHERE FROM_ADDRESS IN ({str_list_add})
                    OR TO_ADDRESS IN ({str_list_add})
                    {string_limit};
                    """
        return sql

    def get_cross_chain_info_sql_query(self, array_address, info_type="label", limit=0):
        """
        Get the sql query to extract the cross chain labels or tags for the array of addresses.
        WARNING you should not provide to much addresses in the array_address parameter because the query may time out.
        Parameters
        ----------
        array_address : array
            The array of addresses to extract
        info_type : str
            The type of info to extract. It can be "label" or "tag"
        limit : int
            The limit of the query default 0 everything is retrieved. The limit is the Keyword LIMIT in SQL.

        Returns
        -------
        sql : str
            The sql query to execute

        """
        str_list_add = self.get_string_address(array_address)
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
                WHERE ADDRESS IN ({str_list_add})
                {string_limit};
                """
        return sql

    @staticmethod
    def get_price_feed_eth_ftm_sql_query(limit=0):
        """
        Get the sql query to extract the price feed for ethereum and fantom tokens starting from 2023-12-11
        Parameters
        ----------
        limit : int
            The limit of the query default 0 everything is retrieved. The limit is the Keyword LIMIT in SQL.

        Returns
        -------

        """
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
