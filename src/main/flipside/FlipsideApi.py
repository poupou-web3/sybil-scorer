from shroomdk import ShroomDK
import pandas as pd


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

    @staticmethod
    def get_string_address(df_address):
        lower_str = ""
        for add in df_address:
            lower_str += f'LOWER(\'{add}\'),'
        lower_str = lower_str[:-1]
        return lower_str

    def get_eth_transactions_sql_query(self, df_address):
        address_list = self.get_string_address(df_address)
        sql = f"""
                SELECT *
                FROM ethereum.core.fact_transactions
                WHERE FROM_ADDRESS IN ({address_list})
                OR TO_ADDRESS IN ({address_list})
                LIMIT 10;
                """
        return sql

    def get_polygon_transactions_sql_query(self, df_address):
        address_list = self.get_string_address(df_address)
        sql = f"""
                SELECT *
                FROM ethereum.core.fact_transactions
                WHERE FROM_ADDRESS IN ({address_list})
                OR TO_ADDRESS IN ({address_list})
                LIMIT 10;
                """
        return sql

    def get_polygon_transactions_sql_query(self, df_address):
        address_list = self.get_string_address(df_address)
        sql = f"""
                SELECT *
                FROM ethereum.core.fact_transactions
                WHERE FROM_ADDRESS IN ({address_list})
                OR TO_ADDRESS IN ({address_list})
                LIMIT 10;
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
