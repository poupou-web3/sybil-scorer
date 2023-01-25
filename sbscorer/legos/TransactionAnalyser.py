import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

absolute_path = os.fspath(Path.cwd().parent.parent.parent)
if absolute_path not in sys.path:
    sys.path.append(absolute_path)


class TransactionAnalyser(object):

    def __init__(self, df_transactions, df_address):
        self.df_transactions = df_transactions
        # holds a df of address/seed wallet so we don't have to create it each time
        self.df_seed_wallet = None
        self.df_address = df_address

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

    def transaction_similitude(self, address, algo_type="address_only", char_tolerance=0):
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
        algo_type : str
            The type of algorithm to use. Default is "address_only" which only use the address to compare.
            options are: address_only, address_and_value
        char_tolerance : int
            The number of character to skip when using the longest common substring algorithm. Default is 0.
            1 may be a good choice when algo_type is "address_and_value".

        Returns
        -------
        has_similar_behavior : bool
            True if the address has similar behavior as another address
        score_similar_behavior : float
            The similarity score of the address
        list_similar_address : map
        The map of address and their similarity score

        """

        # Get all the transactions of the address in a 1D array
        df_address_transactions = self.get_address_transactions(address)
        array_transactions_target = self.get_array_transactions(df_address_transactions, address, algo_type)

        # Get all the transactions from other contributors into an 1D array
        df_other_address = self.df_address[self.df_address['address'] != address]
        for add in df_other_address['address']:
            df_other_address_transactions = self.get_address_transactions(add)
            array_transactions_other = self.get_array_transactions(df_other_address_transactions, add, algo_type)
            df_other_address['lcs'] = self.longest_common_sub_string(array_transactions_target,
                                                                     array_transactions_other,
                                                                     char_tolerance)

        df_similar_address = df_other_address[df_other_address['lcs'] > 5]
        df_similar_address['score'] = df_similar_address['lcs'] / (len(array_transactions_target) / 2)
        df_similar_address['score'] = df_similar_address['score'].apply(lambda x: min(x, 1))
        return df_similar_address

    @staticmethod
    def get_array_transactions(df_address_transactions, address, algo_type="address_only"):
        if algo_type == "address_only":
            array_transactions = df_address_transactions.loc[:, ['from_address', 'to_address']]\
                .replace(address, 'x').values.flatten()
        elif algo_type == "address_and_value":
            array_transactions = df_address_transactions.loc[:, ['from_address', 'value', 'to_address']]\
                .replace(address, 'x').values.flatten()
        else:
            raise ValueError("algo_type must be either address_only or address_and_value")
        return array_transactions

    def has_transaction_similitude(self, address):
        df_similar_address = self.transaction_similitude(address)
        return df_similar_address.shape[0] > 0

    def get_address_transactions(self, address):
        return self.get_address_transactions(self.df_transactions, address)

    def get_address_transactions(self, df, address):
        return df[np.logical_or(self.df_transactions['from_address'] == address,
                                self.df_transactions['to_address'] == address)]

    @staticmethod
    def longest_common_sub_string(target_array, comp_array, char_tolerance=0):

        if char_tolerance == 0:
            m = len(target_array)
            n = len(comp_array)

            dp = [[0 for i in range(m + 1)] for j in range(2)]
            cntr = 0

            for i in range(1, n + 1):
                for j in range(1, m + 1):
                    if target_array[i - 1] == comp_array[j - 1]:
                        dp[i % 2][j] = dp[(i - 1) % 2][j - 1] + 1
                        if dp[i % 2][j] > cntr:
                            cntr = dp[i % 2][j]
                    else:
                        dp[i % 2][j] = 0
            return cntr
        else:
            substring = []
            longest = 0
            for i in range(len(input)):
                c_set = set()
                for j in range(i, len(input)):
                    c_set.add(input[j])
                    if len(c_set) > 2:
                        break
                    if j + 1 - i == longest:
                        substring.append(input[i:j + 1])
                    if j + 1 - i > longest:
                        longest = j + 1 - i
                        substring = []
                        substring.append(input[i:j + 1])
            return len(substring)
