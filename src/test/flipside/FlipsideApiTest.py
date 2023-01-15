import unittest

import sys
import os
from pathlib import Path

import pandas as pd

absolute_path = os.fspath(Path.cwd().parent)
if absolute_path not in sys.path:
    sys.path.append(absolute_path)

from src.main.fliside.FlipsideApi import FlipsideApi


class FlipsideApiTest(unittest.TestCase):
    api_key = os.environ['FLIPSIDE_API_KEY']
    flipside_api = FlipsideApi(api_key)
    PATH_TO_EXAMPLE = "../../../input_example"
    INPUT_CSV = "input.csv"
    path_to_data = os.path.join(PATH_TO_EXAMPLE, INPUT_CSV)
    df_address = pd.read_csv(path_to_data)
    list_unique_address = df_address.address.unique()

    def test_get_string_address(self):
        string_add = self.flipside_api.get_string_address(self.list_unique_address)
        expected = 'LOWER(\'0x76f69dcddd0593b0aff5fd3280c3433ddb68e0d2\'),LOWER(\'0x1bc5ebee4738fd95bd96751c45a90889f772e0f3\'),LOWER(\'0x3812801cbf0e41413db4835a5e36228ad45e32bf\'),LOWER(\'0x8f8a255c64ec0109092674a7219f4d10f625e788\'),LOWER(\'0x5e280efdb4dc45ec4aa73494f78b89a21741a9ba\'),LOWER(\'0xdffe6d135e4396f90ba66a1024bdeb6ef5df9276\'),LOWER(\'0xdcdbd2b5ca6430b2456850cbd2c164413852381a\'),LOWER(\'0xe9034bcd20119ee7563d145dc817820690afd5fb\')'
        self.assertEqual(expected, string_add)

    def test_get_eth_transactions_sql_query(self):
        sql = self.flipside_api.get_eth_transactions_sql_query(self.list_unique_address)
        expected = 'WHERE FROM_ADDRESS IN (LOWER(\'0x76f69dcddd0593b0aff5fd3280c3433ddb68e0d2\'),LOWER(\'0x1bc5ebee4738fd95bd96751c45a90889f772e0f3\'),LOWER(\'0x3812801cbf0e41413db4835a5e36228ad45e32bf\'),LOWER(\'0x8f8a255c64ec0109092674a7219f4d10f625e788\'),LOWER(\'0x5e280efdb4dc45ec4aa73494f78b89a21741a9ba\'),LOWER(\'0xdffe6d135e4396f90ba66a1024bdeb6ef5df9276\'),LOWER(\'0xdcdbd2b5ca6430b2456850cbd2c164413852381a\'),LOWER(\'0xe9034bcd20119ee7563d145dc817820690afd5fb\'))'
        self.assertTrue(expected in sql)

    def test_execute_get_tx_eth(self):
        sql = self.flipside_api.get_eth_transactions_sql_query(self.list_unique_address)
        df = self.flipside_api.execute_query(sql)
        self.assertEqual(10, df.shape[0])


if __name__ == '__main__':
    unittest.main()
