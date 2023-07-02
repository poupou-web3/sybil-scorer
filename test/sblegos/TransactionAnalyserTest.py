import os
import unittest

import pandas as pd

from sbscorer.sblegos.TransactionAnalyser import TransactionAnalyser
from sbscorer.sbutils.LoadData import LoadData


class TransactionAnalyserTest(unittest.TestCase):
    path_to_resources = "../resources"
    path_to_tx = os.path.join(path_to_resources, "transactions")
    dataLoader = LoadData(path_to_tx)
    path_to_test_add = os.path.join(path_to_resources, "test_address")

    df_address = pd.read_csv(os.path.join(path_to_test_add, "tx_analyser_address.csv"))
    df_tx = dataLoader.create_df_tx("ethereum")
    tx_analyser = TransactionAnalyser(df_tx, df_address.address.values)

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

    def test_set_details_in(self):
        self.tx_analyser.set_details_first_incoming_transaction()
        self.assertEqual(
            self.tx_analyser.details_first_incoming_transaction.loc[2, 'first_in_tx_eth_value'], 0.19)

    def test_set_details_out(self):
        self.tx_analyser.set_details_first_outgoing_transaction()
        self.assertEqual(
            self.tx_analyser.details_first_outgoing_transaction.loc[2, 'first_out_tx_eth_value'],
            0.011706)

    def test_has_less_than_n_transactions(self):
        address = "0x000b94c47e4a8d7a70be12c50fc35722a7596972"
        self.assertFalse(self.tx_analyser.has_less_than_n_transactions(address, 10))

    def test_count_transactions(self):
        address = "0x000b94c47e4a8d7a70be12c50fc35722a7596972"
        self.assertEquals(self.tx_analyser.count_transactions(address), 61)

    def test_has_less_than_n_transactions_True(self):
        address = "0xlcsad8bc3dfbe42d9a87686f67c69001a2006da4"
        self.assertTrue(self.tx_analyser.has_less_than_n_transactions(address, 50))

    def test_has_interacted_with_contributor(self):
        address = "0x000b94c47e4a8d7a70be12c50fc35722a7596972"
        self.assertFalse(self.tx_analyser.has_interacted_with_other_contributor(address))

    def test_count_interacted_with_contributor(self):
        address = "0xlcsad8bc3dfbe42d9a87686f67c69001a2006da4"
        self.assertEqual(1, self.tx_analyser.count_interaction_with_other_contributor(address))

    def test_has_interacted_with_contributor_true(self):
        address = "0xlcsad8bc3dfbe42d9a87686f67c69001a2006da4"
        self.assertTrue(self.tx_analyser.has_interacted_with_other_contributor(address))

    def test_get_array_transactions(self):
        add = self.df_address.address.values[0]
        df_address_transactions = self.tx_analyser.get_address_transactions(add)
        array_tx = self.tx_analyser.get_array_transactions(df_address_transactions, add, algo_type="address_only")
        self.assertEqual('x-0x763684e5742a42be570d975a889ba11587432b5c'[:10], array_tx[1])

    def test_transaction_similitude_pylcs(self):
        address = "0x000aa644afae99d06c9a0ed0e41b1e61beca958d"
        tx_sim = self.tx_analyser.transaction_similitude_pylcs(address=address,
                                                               algo_type="address_only")
        self.assertEqual(0, tx_sim.shape[0])

    def test_transaction_similitude_pylcs_true(self):
        address = "0xlcsad8bc3dfbe42d9a87686f67c69001a2006da4"  # copy of 0x000ad8bc3dfbe42d9a87686f67c69001a2006da4
        address_lcs = pd.read_csv(os.path.join(self.path_to_test_add, "tx_analyser_address_lcs.csv"))
        tx_analyser_lcs = TransactionAnalyser(self.df_tx, address_lcs.address.values)
        tx_sim = tx_analyser_lcs.transaction_similitude_pylcs(address=address, algo_type="address_only")
        self.assertEqual(17, tx_sim.loc['0x000ad8bc3dfbe42d9a87686f67c69001a2006da4', 'lcs'])

    def test_transaction_similitude_pylcs_column_name_true(self):
        address = "0xlcsad8bc3dfbe42d9a87686f67c69001a2006da4"  # copy of 0x000ad8bc3dfbe42d9a87686f67c69001a2006da4
        address_lcs = pd.read_csv(os.path.join(self.path_to_test_add, "tx_analyser_address_lcs.csv"))
        tx_analyser_lcs = TransactionAnalyser(self.df_tx, address_lcs.address.values)
        tx_sim = tx_analyser_lcs.transaction_similitude_pylcs(address=address, algo_type="address_only")
        self.assertEqual(17, tx_sim.loc['0x000ad8bc3dfbe42d9a87686f67c69001a2006da4', 'lcs'])

    def test_get_df_features(self):
        df_features = self.tx_analyser.get_df_features()
        self.assertEqual((8, 22), df_features.shape)

    def test_get_df_features_vectorized(self):
        df_features = self.tx_analyser.get_df_features_vectorized()
        self.assertEqual((8, 22), df_features.shape)


if __name__ == '__main__':
    unittest.main()
