from shroomdk import ShroomDK
import pandas as pd
import os

class FlipsideApi(object):

    def __init__(self, api_key):
        self.api_key = api_key

        # Initialize `ShroomDK`
        self.sdk = ShroomDK(api_key)

        # return up to 100,000 results per GET request on the query id
        self.PAGE_SIZE = 100000

        # timeout in minutes
        self.TIMEOUT_MINUTES = 4
        # return results of page 1
        self.PAGE_NUMBER = 1
        # max address to query
        self.MAX_ADDRESS = 100

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
        list_network = ["ethereum", "polygon", "arbitrum", "avalanche", "gnosis", "optimism"]
        for network in list_network:
            self.extract_transactions_net(extract_dir, df_address, network)

    def extract_transactions_net(self, extract_dir, df_address, network):
        print("Extracting transactions for network: ", network)
        len_address = len(df_address)
        q, r = divmod(len_address, self.MAX_ADDRESS)
        if r != 0:
            q += 1
        for i in range(q):
            print(f"Extracting transactions for address: {i * self.MAX_ADDRESS} - {(i + 1) * self.MAX_ADDRESS}")
            df = self.get_transactions(df_address[i * self.MAX_ADDRESS: (i + 1) * self.MAX_ADDRESS], network)
            path_to_export = os.path.join(extract_dir, network)
            if not os.path.exists(path_to_export):
                os.makedirs(path_to_export)
            df.to_csv(os.path.join(path_to_export, f"transactions_{i}.csv"), index=False)

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

    def get_cross_chain_address_labels_sql_query(self, df_address, limit=0):
        address_list = self.get_string_address(df_address)
        if limit != 0:
            string_limit = f"LIMIT {limit}"
        else:
            string_limit = ""
        sql = f"""
                SELECT *
                FROM crosschain.address_labels
                WHERE ADDRESS IN ({address_list})
                {string_limit};
                """
        return sql

    def get_cross_chain_address_tags_sql_query(self, df_address, limit=0):
        address_list = self.get_string_address(df_address)
        if limit != 0:
            string_limit = f"LIMIT {limit}"
        else:
            string_limit = ""
        sql = f"""
                SELECT *
                FROM crosschain.core.address_labels
                WHERE ADDRESS IN ({address_list})
                {string_limit};
                """
        return sql

    def get_price_feed_eth_ftm_sql_query(self, limit=0):
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

# # If the limit is reached in a 5-minute period, the sdk will exponentially back-off and retry the query up to the timeout_minutes parameter set when calling the query method.
# query_result_set = sdk.query(
#     sql,
#     ttl_minutes=60,
#     cached=True,
#     timeout_minutes=20,
#     retry_interval_seconds=1,
#     page_size=5,
#     page_number=2,
# )
