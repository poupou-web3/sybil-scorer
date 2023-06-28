import unittest

import pandas as pd

from sbscorer.sblegos.TransactionAnalyser import TransactionAnalyser


class TransactionAnalyserTestCodium(unittest.TestCase):

    # Tests that the class can be instantiated with a valid dataframe of transactions and addresses
    def test_instantiation(self):
        df_transactions = pd.DataFrame()
        df_address = pd.DataFrame()
        ta = TransactionAnalyser(df_transactions, df_address)
        self.assertIsInstance(ta, TransactionAnalyser)

    # Tests that the set_seed_wallet_naive method sets the seed wallet dataframe correctly
    def test_set_seed_wallet_naive(self):
        df_transactions = pd.DataFrame({
            'from_address': ['0x1', '0x2', '0x3'],
            'to_address': ['0x4', '0x5', '0x6'],
            'block_timestamp': [1, 2, 3],
            'EOA': ['0x1', '0x2', '0x3']
        })

        df_address = pd.DataFrame()
        ta = TransactionAnalyser(df_transactions, df_address)
        ta.set_seed_wallet_naive()
        df_expected_seed = pd.DataFrame({
            'from_address': ['0x1', '0x2', '0x3'],
            'to_address': ['0x4', '0x5', '0x6']
        },
            index=['0x1', '0x2', '0x3'])
        self.assertEqual(ta.df_seed_wallet_naive.to_dict(), df_expected_seed.to_dict())


if __name__ == '__main__':
    unittest.main()
