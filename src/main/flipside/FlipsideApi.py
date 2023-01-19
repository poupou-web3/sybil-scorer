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
        # return results of page 1
        self.PAGE_NUMBER = 1

    def execute_query(self, sql):
        query_result_set = self.sdk.query(sql)
        return pd.DataFrame(query_result_set.records)

    def extract_transactions(self, dir, df_address):

        list_network = ["ethereum", "polygon", "arbitrum", "avalanche", "gnosis", "optimism"]
        for network in list_network:
            print("Extracting transactions for network: ", network)
            df = self.get_transactions(df_address, network)
            csv_dir = os.path.join(dir, network)
            if not os.path.exists(csv_dir):
                os.makedirs(csv_dir)
            df.to_csv(os.path.join(csv_dir, "transactions.csv"))

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
                SELECT *
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
                SELECT *
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
                SELECT *
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
                SELECT *
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
                    SELECT *
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
                    SELECT *
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
