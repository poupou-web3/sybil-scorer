from src.main.flipside.FlipsideApi import FlipsideApi
import unittest

import sys
import os
from pathlib import Path

import pandas as pd

absolute_path = os.fspath(Path.cwd().parent)
if absolute_path not in sys.path:
    sys.path.append(absolute_path)


class FlipsideApiTest(unittest.TestCase):
    api_key = os.environ['FLIPSIDE_API_KEY']
    flipside_api = FlipsideApi(api_key)
    PATH_TO_EXAMPLE = "../../../input_example"
    PATH_TO_TX = "../../../data/transactions"
    INPUT_CSV = "input.csv"
    path_to_data = os.path.join(PATH_TO_EXAMPLE, INPUT_CSV)
    df_address = pd.read_csv(path_to_data)
    list_unique_address = df_address.address.unique()

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
        sql = self.flipside_api.get_cross_chain_address_tags_sql_query(
            self.list_unique_address, limit=10)
        df = self.flipside_api.execute_query(sql)
        self.assertEqual(10, df.shape[0])

    def test_execute_get_labels(self):
        sql = self.flipside_api.get_cross_chain_info_sql_query(self.list_unique_address, limit=10)
        df = self.flipside_api.execute_query(sql)
        self.assertEqual(10, df.shape[0])

    def test_extract_transactions(self):
        self.flipside_api.extract_transactions(self.PATH_TO_TX, self.list_unique_address)
        for network in ["ethereum", "polygon", "optimism", "arbitrum", "avalanche"]:
            df_output = pd.read_csv(os.path.join(os.path.join(self.PATH_TO_TX, network), "transactions_0.csv"))
            self.assertEqual(df_output.shape[1], 8)
        df_output = pd.read_csv(os.path.join(os.path.join(self.PATH_TO_TX, "gnosis", "transactions_0.csv")))
        self.assertEqual(df_output.shape[1], 7)

    def test_get_transactions_ethereum(self):
        df_output = self.flipside_api.get_transactions(self.list_unique_address, "ethereum")
        self.assertTrue(
            '0xc1e0b64374095ae27ca4a98932f03fa3fcfbf60dcece1ca12c71015b21fbedb9' in df_output.tx_hash.values)

    def test_get_transactions_polygon(self):
        df_output = self.flipside_api.get_transactions(self.list_unique_address, "polygon")
        self.assertTrue(
            '0xc1e0b64374095ae27ca4a98932f03fa3fcfbf60dcece1ca12c71015b21fbedb9' in df_output.tx_hash.values)


if __name__ == '__main__':
    unittest.main()
