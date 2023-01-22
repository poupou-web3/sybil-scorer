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
        self.df_seed_wallet = None

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
        df_same_seed = self.get_address_transactions(self.df_seed_wallet, address)
        return df_same_seed.shape[0] > 0

    def set_seed_wallet(self):
        self.df_seed_wallet = self.df_transactions.groupby('to_address').sort_values(
            'block_timestamp', ascending=True).loc['from_address', 'to_address'].first()

    def transaction_similitude(self, address):
        """
        Return a boolean and the list of addresses if it finds other addresses with similar actions.

        The algorithm is the following:
        1. Transform all transactions in to a String of the form: "from_address,
        to_address, from_address, to_address, ..."
        2. Run the algorithm common longest substring on all the transactions
        3. If the longest common substring is longer than 5, return true for the current address.
        4. Keep iterating to find the longest common substring and then the score is
        the length of the longest common substring divided by half the length of the target address string.
        The score is the min(score, 1) to avoid having a score > 1.

        Parameters
        ----------
        address : str
            The address to check

        Returns
        -------
        has_similar_behavior : bool
            True if the address has similar behavior as another address
        score_similar_behavior : float
            The similarity score of the address
        list_similar_address : map
        The map of address and their similarity score

        """

        # Get all the transactions of the address
        df_address_transactions = self.get_address_transactions(address)

        # Get all the transactions from other contributors

    def get_address_transactions(self, address):
        return self.get_address_transactions(self.df_transactions, address)

    def get_address_transactions(self, df, address):
        return df[np.logical_or(self.df_transactions['from_address'] == address,
                                self.df_transactions['to_address'] == address)]
