import os
import unittest

import pandas as pd

from sbscorer.sblegos.TransactionAnalyser import TransactionAnalyser
from sbscorer.utils.LoadData import LoadData


class TransactionAnalyserTest(unittest.TestCase):
    path_to_resources = "../resources"
    path_to_tx = os.path.join(path_to_resources, "transactions")
    dataLoader = LoadData(path_to_tx)
    path_to_test_add = os.path.join(path_to_resources, "test_address")

    df_address = pd.read_csv(os.path.join(path_to_test_add, "tx_analyser_address.csv"))
    df_tx = dataLoader.create_df_tx("ethereum")
    tx_analyser = TransactionAnalyser(df_tx, df_address)

    def test_has_same_seed_naive(self):
        address = "0x000bec82c41837d974899b26b26f9cc8890af9ea"
        self.assertFalse(self.tx_analyser.has_same_seed_naive(address))

    def test_has_same_seed_naive_True(self):
        address = "0x000aa644afae99d06c9a0ed0e41b1e61beca958d"
        self.assertTrue(self.tx_analyser.has_same_seed_naive(address))

    def test_has_same_seed_naive_biased(self):
        address = "0x000b94c47e4a8d7a70be12c50fc35722a7596972"
        self.assertFalse(self.tx_analyser.has_same_seed_naive(address))

    def test_has_same_seed_naive_True_biased(self):
        address = "0x000b94c47e4a8d7a70be12c50fc35722a7596972"
        self.assertFalse(self.tx_analyser.has_same_seed_naive(
            address))  # this one is false because it is not looking at the right address

    def test_has_same_seed_True(self):
        address = "0x000b94c47e4a8d7a70be12c50fc35722a7596972"
        self.assertTrue(self.tx_analyser.has_same_seed(address))

    def test_has_same_seed_True(self):
        address = "0x000b94c47e4a8d7a70be12c50fc35722a7596972"
        self.assertTrue(self.tx_analyser.has_suspicious_seed_behavior(address))

    def test_get_array_transactions(self):
        add = self.df_address.address.values[0]
        df_address_transactions = self.tx_analyser.get_address_transactions(add)
        array_tx = self.tx_analyser.get_array_transactions(df_address_transactions, add, algo_type="address_only")
        self.assertEqual('x', array_tx[1])

    def test_transaction_similitude(self):
        address = "0x000aa644afae99d06c9a0ed0e41b1e61beca958d"
        tx_sim = self.tx_analyser.transaction_similitude(address=address, algo_type="address_only", char_tolerance=0)
        self.assertEqual(0, tx_sim.shape[0])

    def test_transaction_similitude_true(self):
        address = "0xlcsad8bc3dfbe42d9a87686f67c69001a2006da4"  # copy of 0x000ad8bc3dfbe42d9a87686f67c69001a2006da4
        address_lcs = pd.read_csv(os.path.join(self.path_to_test_add, "tx_analyser_address_lcs.csv"))
        tx_analyser_lcs = TransactionAnalyser(self.df_tx, address_lcs)
        tx_sim = tx_analyser_lcs.transaction_similitude(address=address, algo_type="address_only", char_tolerance=0)
        self.assertEqual(52, tx_sim.loc['0x000ad8bc3dfbe42d9a87686f67c69001a2006da4', 'lcs'])

    def test_transaction_similitude_opti(self):
        address = "0x000aa644afae99d06c9a0ed0e41b1e61beca958d"
        tx_sim = self.tx_analyser.transaction_similitude_opti(address=address,
                                                              algo_type="address_only",
                                                              char_tolerance=0)
        self.assertEqual(0, tx_sim.shape[0])

    def test_transaction_similitude_opti_true(self):
        address = "0xlcsad8bc3dfbe42d9a87686f67c69001a2006da4"  # copy of 0x000ad8bc3dfbe42d9a87686f67c69001a2006da4
        address_lcs = pd.read_csv(os.path.join(self.path_to_test_add, "tx_analyser_address_lcs.csv"))
        tx_analyser_lcs = TransactionAnalyser(self.df_tx, address_lcs)
        tx_sim = tx_analyser_lcs.transaction_similitude(address=address, algo_type="address_only", char_tolerance=0)
        self.assertEqual(52, tx_sim.loc['0x000ad8bc3dfbe42d9a87686f67c69001a2006da4', 'lcs'])


if __name__ == '__main__':
    unittest.main()
