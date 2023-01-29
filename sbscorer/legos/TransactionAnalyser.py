import os
import sys
from pathlib import Path

import numpy as np

absolute_path = os.fspath(Path.cwd().parent.parent.parent)
if absolute_path not in sys.path:
    sys.path.append(absolute_path)


class TransactionAnalyser(object):

    def __init__(self, df_transactions, df_address):
        self.df_transactions = df_transactions
        # holds a df of address/seed wallet so we don't have to create it each time
        self.df_seed_wallet_naive = None
        self.df_seed_wallet = None
        self.gb_EOA_sorted = None
        self.df_address = df_address
        # We use a df address so we can load all transactions in memmory and then change the address list easily
        # for example to calculate on a specific project

    def has_same_seed_naive(self, address):
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

        if self.df_seed_wallet_naive is None:
            self.set_seed_wallet_naive()
        df_same_seed = self.get_address_same_seed(self.df_seed_wallet_naive, address)
        return df_same_seed.shape[0] > 0

    def has_same_seed(self, address):
        """Return if the address has the same seed wallet as one of the seed wallet of the df_transactions
        using a non-naive algorithm.
        For some address the first transaction is not the incomming funding transaction.
        It is possible to interact with a smart contract even before receiving any fund.
        This algorithm takes that into account.

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

        if self.df_seed_wallet_naive is None:
            self.set_seed_wallet()
        df_same_seed = self.get_address_same_seed(self.df_seed_wallet, address)
        return df_same_seed.shape[0] > 0

    @staticmethod
    def get_address_same_seed(df, address):
        seed_add = df.loc[address, 'from_address']
        df_same_seed = df.drop(address, axis=0).loc[
            df.drop(address, axis=0)['from_address'] == seed_add]
        return df_same_seed

    def has_suspicious_seed_behavior(self, address):
        return self.has_same_seed(address) != self.has_same_seed_naive(address)

    def set_seed_wallet_naive(self):
        if self.gb_EOA_sorted is None:
            self.set_group_by_sorted_EOA()
        self.df_seed_wallet_naive = self.gb_EOA_sorted.first().loc[:, ['from_address', 'to_address']]

    def set_seed_wallet(self):
        df_filtered = self.df_transactions[self.df_transactions['EOA'] == self.df_transactions['to_address']]
        df_gb = df_filtered.sort_values('block_timestamp', ascending=True).groupby('EOA')
        self.df_seed_wallet = df_gb.first().loc[:, ['from_address', 'to_address']]

    def set_group_by_sorted_EOA(self):
        self.gb_EOA_sorted = self.df_transactions.sort_values('block_timestamp', ascending=True).groupby('EOA')

    def transaction_similitude(self, address, algo_type="address_only", char_tolerance=0):
        """
        Return a boolean and the list of addresses if it finds other addresses with similar actions.

        The algorithm is the following:
        1. Transform all transactions in to a String of the form: "from_address,
        to_address, from_address, to_address, ..."
        2. Replace the address of the wallet by "x" to ba able to compare the behavior of two addresses.
        3. Run the algorithm common longest substring on all the transactions
        4. If the longest common substring is longer than 5, return true for the current address.
        5. Keep iterating to find the longest common substring and then the score is
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
        df_other_address = self.df_address.loc[self.df_address['address'] != address, :]
        df_other_address['lcs'] = 0
        df_other_address.set_index('address', inplace=True)
        for add in df_other_address.index:
            df_other_address_transactions = self.get_address_transactions(add)
            if df_other_address_transactions.shape[0] <= 1:
                df_other_address.loc[add, 'lcs'] = 0
            else:
                array_transactions_other = self.get_array_transactions(df_other_address_transactions, add, algo_type)
                lcs = self.longest_common_sub_string(array_transactions_target, array_transactions_other,
                                                     char_tolerance)
                df_other_address.loc[add, 'lcs'] = lcs

        df_similar_address = df_other_address.loc[df_other_address['lcs'] > 5, :]
        df_similar_address['score'] = df_similar_address.loc[:, 'lcs'].apply(
            lambda x: min(x / (len(array_transactions_target) / 2), 1))
        return df_similar_address

    @staticmethod
    def get_array_transactions(df_address_transactions, address, algo_type="address_only"):
        """
        This method replace the target address by an arbitrary "x" to be able to compare the similitude of two wallet.

        Parameters
        ----------
        df_address_transactions : pd.DataFrame
            The data frame of transactions

        address :  str
            The address to replace by x

        algo_type : str
            The type of algorithm to use,
                "address_only" only return from_address and to_address with the address replaced by x
                "address_and_value" return from_address, value, to_address with the address replaced by x

        Returns
        -------
        array_transactions : narray
            An array of strings

        """
        df_address_transactions.sort_values('block_timestamp', ascending=True, inplace=True)
        if algo_type == "address_only":
            array_transactions = df_address_transactions.loc[:, ['from_address', 'to_address']] \
                .replace(address, 'x').values.flatten()
        elif algo_type == "address_and_value":
            array_transactions = df_address_transactions.loc[:, ['from_address', 'value', 'to_address']] \
                .replace(address, 'x').values.flatten()
        else:
            raise ValueError("algo_type must be either address_only or address_and_value")
        return array_transactions

    def has_transaction_similitude(self, address):
        df_similar_address = self.transaction_similitude(address)
        return df_similar_address.shape[0] > 0

    def get_address_transactions(self, address):
        """
        Get transactions of an address from the self.df_transaction df
        Parameters
        ----------
        address : str
            The address to retrieve transactions

        Returns
        -------
        df : pd.DataFrame
            The data frame with the transactions of the address

        """
        return self.get_address_transactions_add(self.df_transactions, address)

    def get_address_transactions_add(self, df, address):
        """
        Get transactions of an address from a dataframe df
        Parameters
        ----------
        df : pd.dataFrame
            Data frame of transactions with the 'EOA' column

        address : str
            The address to retrieve transactions

        Returns
        -------
        df : pd.DataFrame
            The data frame with the transactions of the address

        """
        return df[self.df_transactions['EOA'] == address]

    @staticmethod
    def longest_common_sub_string(target_array, comp_array, char_tolerance=0):

        if char_tolerance == 0:
            m = len(comp_array)
            n = len(target_array)
            # dp will store solutions as the iteration goes on
            dp = np.zeros((2, m + 1), dtype=int)

            res = 0

            for i in range(1, n + 1):
                for j in range(1, m + 1):
                    if target_array[i - 1] == comp_array[j - 1]:
                        dp[i % 2][j] = dp[(i - 1) % 2][j - 1] + 1
                        if dp[i % 2][j] > res:
                            res = dp[i % 2][j]
                    else:
                        dp[i % 2][j] = 0
            return res

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

        @staticmethod
        def longest_common_sub_sequence(target_array, comp_array, char_tolerance=0):

            if char_tolerance == 0:
                m = len(target_array)
                n = len(comp_array)
                # dp will store solutions as the iteration goes on
                dp = np.zeros((m + 1, n + 1), dtype=int)

                for i in range(m + 1):
                    for j in range(n + 1):
                        if i == 0 or j == 0:
                            dp[i][j] = 0
                        elif target_array[i - 1] == comp_array[j - 1]:
                            dp[i][j] = dp[i - 1][j - 1] + 1
                        else:
                            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                return dp[m][n]

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
