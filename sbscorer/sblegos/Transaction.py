import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

absolute_path = os.fspath(Path.cwd().parent.parent.parent)
if absolute_path not in sys.path:
    sys.path.append(absolute_path)


class Transaction(object):
    """
    This class is used to analyse transactions of an address.
    It has methods that allows to perform on chain analysis of an address.
    """

    def __init__(self, df_transactions, array_address=None):
        """
        This class is used to analyse transactions of an address.
        It has methods that allows to perform on chain analysis of an address.

        It is initialized with a df_transactions containing all the transactions made by a list of addresses that
        should match the df_transactions
        Parameters
        ----------
        df_transactions : pd.DataFrame
            The dataframe containing all the transactions of the addresses
        array_address : np.ndarray
            The ndarray containing a list of addresses
        """
        assert isinstance(df_transactions, pd.DataFrame), "The df_transactions should be a pd.DataFrame"

        columns = df_transactions.columns
        assert 'block_timestamp' in columns, "The df_transactions should have a column named 'block_timestamp'"
        assert 'value' in columns, "The df_transactions should have a column named 'value'"
        assert 'gas_limit' in columns, "The df_transactions should have a column named 'gas_limit'"
        assert 'tx_fee' in columns, "The df_transactions should have a column named 'tx_fee'"
        assert 'gas_used' in columns, "The df_transactions should have a column named 'gas_used'"
        assert 'block_number' in columns, "The df_transactions should have a column named 'block_number'"
        assert 'from_address' in columns, "The df_transactions should have a column named 'from_address'"
        assert 'to_address' in columns, "The df_transactions should have a column named 'to_address'"

        if 'eoa' not in columns:
            tmp_df_tx = df_transactions.copy()
            print("Creating eoa column")
            tmp_df_tx = pd.concat(tmp_df_tx, tmp_df_tx)
            tmp_df_tx['eoa'] = np.concatenate((tmp_df_tx['from_address'].values,
                                               tmp_df_tx['to_address'].values))
        else:
            tmp_df_tx = df_transactions

        if array_address is None:
            self.array_address = tmp_df_tx['eoa'].unique()
            self.df_transactions = tmp_df_tx
        else:
            assert isinstance(array_address, np.ndarray), "The array_address should be a numpy array"
            self.array_address = np.intersect1d(array_address, tmp_df_tx['eoa'].unique())
            self.df_transactions = df_transactions[tmp_df_tx['eoa'].isin(array_address)]
