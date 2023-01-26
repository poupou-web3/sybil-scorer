import os
import sys
import unittest
from pathlib import Path

import pandas as pd

from sbscorer.flipside.FlipsideApi import FlipsideApi

absolute_path = os.fspath(Path.cwd().parent)
if absolute_path not in sys.path:
    sys.path.append(absolute_path)


class FlipsideApiTest(unittest.TestCase):
    api_key = os.environ['FLIPSIDE_API_KEY']
    flipside_api = FlipsideApi(api_key, max_address=100)
    PATH_TO_RESOURCES = "../resources"
    PATH_TO_TEST_ADDRESS = os.path.join(PATH_TO_RESOURCES, "test_address")
    PATH_TO_TMP_TX = os.path.join(PATH_TO_RESOURCES, "tmp/transactions")
    PATH_TO_TMP_TX_LARGE = os.path.join(PATH_TO_RESOURCES, "tmp/transactions_large")
    INPUT_CSV = "address.csv"
    TEST_CSV_ADD = "flipside_test_address.csv"
    TEST_CSV_ADD_LARGE = "unique_ctbt_address.csv"

    df_address = pd.read_csv(os.path.join(PATH_TO_TEST_ADDRESS, INPUT_CSV))
    list_unique_address = df_address.address.unique()

    df_test_address = pd.read_csv(os.path.join(PATH_TO_TEST_ADDRESS, TEST_CSV_ADD))
    test_address = df_test_address.address.values

    df_test_address_large = pd.read_csv(os.path.join(PATH_TO_TEST_ADDRESS, TEST_CSV_ADD_LARGE))
    test_address_large = df_test_address_large.address.values[:900]

    def test_get_string_address(self):
        string_add = self.flipside_api.get_string_address(
            self.list_unique_address)
        expected = 'LOWER(\'0x06cd8288dc001024ce0a1cf39caaedc0e2db9c82\'),LOWER(\'0x9be7d88cfd6e4b519cd9720db6de6e6f2c1ca77e\'),LOWER(\'0xf8bde71eb161bd83da88bd3a1003eef9ba0c7485\'),LOWER(\'0x1994bc4f630a373ffc3ecef84165cfb85e7f7820\'),LOWER(\'0x13ef1086cdfecc00e0f8f3b2ac2c600f297dc333\'),LOWER(\'0xb324b8ab8634a6c160361d34e672cec739ac55cd\'),LOWER(\'0x1b7a0da1d9c63d9b8209fa5ce98ac0d148960800\'),LOWER(\'0xe718bb18d8176659606b3d7d3f705906a9d3e1bd\')'
        self.assertEqual(expected, string_add)

    def test_get_eth_transactions_sql_query(self):
        sql = self.flipside_api.get_eth_transactions_sql_query(
            self.list_unique_address)
        expected = 'WHERE FROM_ADDRESS IN (LOWER(\'0x06cd8288dc001024ce0a1cf39caaedc0e2db9c82\'),LOWER(\'0x9be7d88cfd6e4b519cd9720db6de6e6f2c1ca77e\'),LOWER(\'0xf8bde71eb161bd83da88bd3a1003eef9ba0c7485\'),LOWER(\'0x1994bc4f630a373ffc3ecef84165cfb85e7f7820\'),LOWER(\'0x13ef1086cdfecc00e0f8f3b2ac2c600f297dc333\'),LOWER(\'0xb324b8ab8634a6c160361d34e672cec739ac55cd\'),LOWER(\'0x1b7a0da1d9c63d9b8209fa5ce98ac0d148960800\'),LOWER(\'0xe718bb18d8176659606b3d7d3f705906a9d3e1bd\'))'
        self.assertTrue(expected in sql)

    def test_execute_get_tx_eth(self):
        sql = self.flipside_api.get_eth_transactions_sql_query(
            self.list_unique_address, limit=10)
        df = self.flipside_api.execute_query(sql)
        self.assertEqual(10, df.shape[0])

    def test_execute_get_tx_polygon(self):
        sql = self.flipside_api.get_polygon_transactions_sql_query(
            self.list_unique_address, limit=10)
        df = self.flipside_api.execute_query(sql)
        self.assertEqual(10, df.shape[0])

    def test_execute_get_tx_optimism(self):
        sql = self.flipside_api.get_optimism_transactions_sql_query(
            self.list_unique_address, limit=10)
        df = self.flipside_api.execute_query(sql)
        self.assertEqual(10, df.shape[0])

    def test_execute_get_tx_arbitrum(self):
        sql = self.flipside_api.get_arbitrum_transactions_sql_query(
            self.list_unique_address, limit=10)
        df = self.flipside_api.execute_query(sql)
        self.assertEqual(10, df.shape[0])

    def test_execute_get_tx_gnosis(self):
        sql = self.flipside_api.get_gnosis_transactions_sql_query(
            self.list_unique_address, limit=10)
        df = self.flipside_api.execute_query(sql)
        self.assertEqual(10, df.shape[0])

    def test_execute_get_tx_avalanche(self):
        sql = self.flipside_api.get_avalanche_transactions_sql_query(
            self.list_unique_address, limit=10)
        df = self.flipside_api.execute_query(sql)
        self.assertEqual(10, df.shape[0])

    def test_execute_get_tags(self):
        sql = self.flipside_api.get_cross_chain_info_sql_query(
            self.list_unique_address,
            info_type="tag",
            limit=10)
        df = self.flipside_api.execute_query(sql)
        self.assertEqual(0, df.shape[1])  # no tags or labels in the example

    def test_execute_get_labels(self):
        sql = self.flipside_api.get_cross_chain_info_sql_query(
            self.list_unique_address,
            info_type="label",
            limit=10)
        df = self.flipside_api.execute_query(sql)
        self.assertEqual(0, df.shape[1])

    @unittest.skip("TODO change test very long running")
    def test_extract_transactions(self):
        self.flipside_api.extract_transactions(self.PATH_TO_TMP_TX, self.list_unique_address)
        for network in ["ethereum"]:
            df_output = pd.read_csv(os.path.join(
                os.path.join(self.PATH_TO_TMP_TX, network),
                "0xf8bde71eb161bd83da88bd3a1003eef9ba0c7485_tx.csv"))
            self.assertEqual(df_output.shape[1], 8)

    def test_extract_tx_eth(self):
        tx_chain = "ethereum"
        self.flipside_api.extract_transactions_net(self.PATH_TO_TMP_TX, self.test_address, tx_chain)
        df_output = pd.read_csv(os.path.join(
            os.path.join(self.PATH_TO_TMP_TX, tx_chain),
            "0x000aa644Afae99d06C9a0ED0E41B1e61bECA958d_tx.csv"))
        df_filter = df_output[df_output["block_timestamp"] <= '2023-01-01']
        self.assertEqual(133, df_filter.shape[0])

    def test_extract_large_tx_eth(self):
        tx_chain = "ethereum"
        flipside_api_large = FlipsideApi(self.api_key, max_address=1000)
        df_output = flipside_api_large.get_transactions(self.test_address_large, tx_chain)
        df_filter = df_output[df_output["block_timestamp"] <= '2023-01-01']
        self.assertEqual(107031, df_filter.shape[0])  # 100k transactions the maximum per_page of flipside api

    def test_get_transactions_ethereum(self):
        df_output = self.flipside_api.get_transactions(self.list_unique_address, "ethereum")
        self.assertTrue(
            '0xc1e0b64374095ae27ca4a98932f03fa3fcfbf60dcece1ca12c71015b21fbedb9' in df_output.tx_hash.values)

    def test_get_transactions_polygon(self):
        df_output = self.flipside_api.get_transactions(self.list_unique_address, "polygon")
        self.assertTrue(
            '0xe55e3bf2459b3620e3cb54000832e57ce87aa609d759a33459dfbdb84a655741' in df_output.sort_values(
                "block_timestamp").tx_hash.values)


if __name__ == '__main__':
    unittest.main()
