import os
import unittest

import pandas as pd

from sbscorer.legos.TransactionAnalyser import TransactionAnalyser
from sbscorer.utils.LoadData import LoadData


class TransactionAnalyserTest(unittest.TestCase):
    path_to_resources = "../resources"
    path_to_tx = os.path.join(path_to_resources, "transactions")
    dataLoader = LoadData(path_to_tx)
    path_to_test_add = os.path.join(path_to_resources, "test_address")

    df_address = pd.read_csv(os.path.join(path_to_test_add, "unique_address.csv"))
    df_tx = dataLoader.create_df_tx("ethereum")
    tx_analyser = TransactionAnalyser(df_tx, df_address)

    def test_has_same_seed(self):
        address = "0x000bec82c41837d974899b26b26f9cc8890af9ea"
        self.assertFalse(self.tx_analyser.has_same_seed(address))

    def test_has_same_seed_True(self):
        address = "0x000aa644afae99d06c9a0ed0e41b1e61beca958d"
        self.assertTrue(self.tx_analyser.has_same_seed(address))


if __name__ == '__main__':
    unittest.main()
