from src.main.flipside.FlipsideApi import FlipsideApi
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

absolute_path = os.fspath(Path.cwd().parent.parent.parent)
if absolute_path not in sys.path:
    sys.path.append(absolute_path)


class TransactionAnalyser(object):

    def __init__(self, df_transactions):
        self.df_transactions = df_transactions
        # holds a df of address/seed wallet so we don't have to create it each time

    def has_same_seed(self, address):
        """Return if the address has the same seed wallet as one of the seed wallet of the df_transactions

            If the df_seed_wallet is not set, it will set it
            Note df_transaction could contain transactions from multiple network but the seed wallet of the address is
             filtered which prevent unexpected raise of the boolean.

            Parameters
            ----------
            address : str
                The address to check

            Returns
            -------
            has_same_seed : bool
            True if the address has the same seed wallet as one of the seed wallet of the df_transactions
        """

        if self.df_seed_wallet is None:
            self.set_seed_wallet()
        df_same_seed = self.df_seed_wallet[np.logical_and(
            self.df_seed_wallet['from_address'] == address,
            self.df_seed_wallet['to_address'] != address)]
        return df_same_seed.shape[0] > 0

    def set_seed_wallet(self):
        df_seed_wallet = self.df_transactions.groupby('to_address').sort_values(
            'block_timestamp', ascending=True).loc['from_address', 'to_address'].first()
