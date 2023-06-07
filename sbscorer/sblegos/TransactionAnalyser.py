import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pylcs

absolute_path = os.fspath(Path.cwd().parent.parent.parent)
if absolute_path not in sys.path:
    sys.path.append(absolute_path)


class TransactionAnalyser(object):
    """
    This class is used to analyse transactions of an address.
    It has methods that allows to perform on chain analysis of an address.
    """

    def __init__(self, df_transactions, df_address):
        """
        This class is used to analyse transactions of an address.
        It has methods that allows to perform on chain analysis of an address.

        It is initialized with a df_transactions containing all the transactions made by a list of addresses that
        should match the df_transactions
        Parameters
        ----------
        df_transactions : pd.DataFrame
            The dataframe containing all the transactions of the addresses
        df_address : pd.DataFrame
            The dataframe containing a 'address' column 
        """
        self.df_transactions = df_transactions
        # holds a df of address/seed wallet we don't have to create it each time
        self.df_seed_wallet_naive = None
        self.df_seed_wallet = None
        self.gb_EOA_sorted = None
        self.df_address = df_address
        # We use a df address we can load all transactions in memory and then change the address list easily
        # for example to calculate on a specific project

        # store the array of string transactions
        self.dict_add_string_tx = None
        self.dict_add_value_string_tx = None

    def has_same_seed_naive(self, address):
        """
        Return if the address has the same seed wallet as one of the seed wallet of the df_transactions

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
        """
        Return if the address has the same seed wallet as one of the seed wallet of the df_transactions
        using a non-naive algorithm.
        For some address the first transaction is not the incoming funding transaction.
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

        if self.df_seed_wallet is None:
            self.set_seed_wallet()
        if address in self.df_seed_wallet.to_address.values:
            df_same_seed = self.get_address_same_seed(self.df_seed_wallet, address)
            return df_same_seed.shape[0] > 0
        else:
            return False

    @staticmethod
    def get_address_same_seed(df, address):
        """
        Return a df of address that have the same seed wallet as the address given in parameter.
        Parameters
        ----------
        df : pd.DataFrame
            The df to filter
        address : str
            The address to check
        Returns
        -------
        df_same_seed : pd.DataFrame
            The df of address that have the same seed wallet as the address given in parameter.

        """
        seed_add = df.loc[address, 'from_address']
        df_same_seed = df.drop(address, axis=0).loc[
            df.drop(address, axis=0)['from_address'] == seed_add]
        return df_same_seed

    def has_suspicious_seed_behavior(self, address):
        """
        Return a boolean whether the address has suspicious seed behavior.
        Most addresses have a seed wallet that is given by first transaction given by the naive algorithm.
        However, some addresses first transaction is no the first incoming transaction because they first interacted
        with a smart contract. This is a suspicious behavior.
        Parameters
        ----------
        address : str
            The address to check

        Returns
        -------
        has_suspicious_seed_behavior : bool
            True if the address has suspicious seed behavior
        """
        return self.has_same_seed(address) != self.has_same_seed_naive(address)

    def set_seed_wallet_naive(self):
        """
        Set the df_seed_wallet_naive attribute of the class. It holds the seed wallet of the addresses in 'EOA' using
        a naive method that takes the from_address from the transaction of the address

        Returns
        -------
        None
            Set the df_seed_wallet_naive attribute of the class

        """
        if self.gb_EOA_sorted is None:
            self.set_group_by_sorted_EOA()
        self.df_seed_wallet_naive = self.gb_EOA_sorted.first().loc[:, ['from_address', 'to_address']]

    def set_seed_wallet(self):
        """
        Set the df_seed_wallet attribute of the class. It holds the seed wallet of the addresses in 'EOA'
        of df_transactions. It is a non-naive method that look for the first incoming transaction of the address to get
        the seed wallet.
        Returns
        -------
        None
            Set the df_seed_wallet attribute of the class
        """
        df_filtered = self.df_transactions[self.df_transactions['EOA'] == self.df_transactions['to_address']]
        df_gb = df_filtered.sort_values('block_timestamp', ascending=True).groupby('EOA')
        self.df_seed_wallet = df_gb.first().loc[:, ['from_address', 'to_address']]

    def set_group_by_sorted_EOA(self):
        """
        Set the gb_EOA_sorted attribute of the class it holds the df_transactions sorted by block_timestamp and
        grouped by EOA

        Returns
        -------
        None
            Set the gb_EOA_sorted attribute of the class

        """
        if self.gb_EOA_sorted is None:
            self.gb_EOA_sorted = self.df_transactions.sort_values('block_timestamp', ascending=True).groupby('EOA')

    def has_less_than_n_transactions(self, address, n=5):
        """
        Return a boolean whether the address has less than n transactions
        Parameters
        ----------
        address : str
            The address to check
        n : int
            The number of transactions

        Returns
        -------
        has_less_than_n_transactions : bool
            True if the address has less than n transactions
        """
        self.set_group_by_sorted_EOA()
        return self.gb_EOA_sorted.get_group(address).shape[0] < n

    def has_interacted_with_other_contributor(self, address):
        """
        Return a boolean whether the address has interacted with other contributor (not itself)
        Parameters
        ----------
        address : str
            The address to check

        Returns
        -------
        has_interacted_with_other_contributor : bool
            True if the address has interacted with one or more contributor of the grant
        """
        self.set_group_by_sorted_EOA()
        contributors = self.get_contributors()
        other_contributors = contributors[contributors != address]

        df = self.gb_EOA_sorted.get_group(address)
        add_interacted = np.append(df['to_address'].to_numpy(), df['from_address'].to_numpy())
        add_interacted = add_interacted.astype('str')
        unique_add_interacted = np.unique(add_interacted)
        unique_add_interacted = unique_add_interacted[unique_add_interacted != address]
        return np.isin(unique_add_interacted, other_contributors).any()

    def get_contributors(self):
        """
        Return a list of contributors of the grant
        Returns
        -------
        contributors : narray
            The array of contributors of the grant
        """
        return self.df_transactions['EOA'].unique()

    def transaction_similitude_pylcs(self, address, algo_type="address_only", minimum_sim_tx=5):
        """
        Return a boolean and the list of addresses if it finds other addresses with similar actions.
        it first stores some repetitive tasks into a class attribute and then use it to speed up the process.

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
        minimum_sim_tx : int
            The number of transactions to use to compare. Default is 5.
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

        # Transform all transactions into a 1D string
        if algo_type == "address_only":
            if self.dict_add_string_tx is None:
                self.set_dict_add_string_transactions(algo_type)
            str_transactions_target = self.dict_add_string_tx.get(address)
        elif algo_type == "address_and_value":
            if self.dict_add_value_string_tx is None:
                self.set_dict_add_string_transactions(algo_type)
            # Get all the transactions of the address in a 1D array
            str_transactions_target = self.dict_add_value_string_tx.get(address)
        else:
            Exception("algo_type not supported")

        shape_target = self.get_address_transactions(address).shape[0]
        min_shape = max(1, shape_target / 4)
        max_shape = max(shape_target, shape_target * 3)

        if self.df_address.columns != ['address']:
            self.df_address.columns = ['address']
        list_lcs = []
        for add in self.df_address['address']:
            if add != address:
                shape_other = self.get_address_transactions(add).shape[0]
                if min_shape < shape_other < max_shape:  # Heuristic to avoid comparing addresses with too different shapes
                    if algo_type == "address_only":
                        str_transactions_other = self.dict_add_string_tx.get(add)
                    else:
                        str_transactions_other = self.dict_add_value_string_tx.get(add)
                    lcs = self.longest_common_sub_string_pylcs(str_transactions_target, str_transactions_other)
                    list_lcs.append(lcs)
                else:
                    list_lcs.append(0)
            else:
                list_lcs.append(0)

        if minimum_sim_tx == -1:
            mask = np.array(list_lcs) > max(3, min(10, shape_target / 4))
        else:
            mask = np.array(list_lcs) > minimum_sim_tx
        df_similar_address = self.df_address.loc[mask, :].copy()
        df_similar_address['lcs'] = np.array(list_lcs)[mask]
        len_tx = len(str_transactions_target) / 2  # Divide by 2 because we have from_address and to_address
        df_similar_address['score'] = df_similar_address.loc[:, 'lcs'].apply(
            lambda x: min(x / len_tx, 1))
        return df_similar_address.set_index('address')

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
            try:
                array_transactions = df_address_transactions.loc[:, ['from_address', 'to_address']].dropna() \
                    .apply(lambda x: x.str[:8]) \
                    .replace(address[:8], 'x') \
                    .agg('-'.join, axis=1) \
                    .values
            except Exception as e:
                array_transactions = []
        elif algo_type == "address_and_value":
            try:
                array_transactions = df_address_transactions.loc[:, ['from_address', 'value', 'to_address']].dropna() \
                    .apply(lambda x: x.str[:8]) \
                    .replace(address, 'x') \
                    .agg('-'.join, axis=1) \
                    .values
            except Exception as e:
                array_transactions = []
        else:
            raise ValueError("algo_type must be either address_only or address_and_value")
        return array_transactions

    def get_address_transactions(self, address):
        """
        Get transactions of an address from the self.df_transaction df using the group by
        Parameters
        ----------
        address : str
            The address to retrieve transactions

        Returns
        -------
        df : pd.DataFrame
            The data frame with the transactions of the address

        """
        try:
            df = self.gb_EOA_sorted.get_group(address)
        except Exception as e:
            if self.gb_EOA_sorted is None:
                self.set_group_by_sorted_EOA()
                df = self.get_address_transactions(address)
            else:
                df = pd.DataFrame()
        return df

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

    def set_dict_add_string_transactions(self, algo_type="address_only"):
        """
        This method create a dictionary with the address as key and the array of transactions as value.
        The array of transactions is the array crated with the get_array_transactions method.
        Parameters
        ----------
        algo_type : str
            The type of algorithm to use

        Returns
        -------
        None
            it sets the self.dict_add_string_tx or self.dict_add_value_string_tx attribute
        """

        if self.gb_EOA_sorted is None:
            gb_address = self.df_transactions.groupby('EOA')
        else:
            gb_address = self.gb_EOA_sorted

        if algo_type == "address_only":
            if self.dict_add_string_tx is None:
                self.dict_add_string_tx = self.get_dict_string_tx(gb_address, algo_type=algo_type)
        elif algo_type == "address_and_value":
            if self.dict_add_value_string_tx is None:
                self.dict_add_value_string_tx = self.get_dict_string_tx(gb_address, algo_type=algo_type)
        else:
            raise ValueError("algo_type must be either address_only or address_and_value")

    def get_dict_string_tx(self, gb_address, algo_type="address_only"):
        dict_string_tx = {}
        for address, df_address in gb_address:
            array_transactions = self.get_array_transactions(df_address, address, algo_type)
            dict_string_tx[address] = "".join(array_transactions)
        return dict_string_tx

    @staticmethod
    def longest_common_sub_string_pylcs(string_target, string_other):

        # 1 similar transaction equals to 8 first char of the address + "-" + "x" = 10 char
        lcs = pylcs.lcs_string_length(string_target, string_other)
        return lcs // 10  # quotient of the division
