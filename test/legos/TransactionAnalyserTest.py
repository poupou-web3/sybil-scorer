import os
import unittest

import pandas as pd

from sbscorer.legos.TransactionAnalyser import TransactionAnalyser
from sbscorer.utils.LoadData import LoadData


class TransactionAnalyserTest(unittest.TestCase):
    path_to_resources = "../resources"
    path_to_tx = os.path.join(path_to_resources, "transactions")
    dataLoader = LoadData(path_to_tx)

    df_address = pd.read_csv(os.path.join(path_to_resources, "unique_address.csv"))
    df_tx = dataLoader.create_df_tx("ethereum")
    tx_analyser = TransactionAnalyser(df_tx, df_address)

    def test_has_same_seed(self):
        address = "0x00000bec592ec7c143c73dc85804962075827ecc"
        self.assertFalse(self.tx_analyser.has_same_seed(address))


if __name__ == '__main__':
    unittest.main()
