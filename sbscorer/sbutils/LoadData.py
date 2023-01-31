import os

import pandas as pd


class LoadData(object):
    """
    This class contain a set of methods to load data from the csv files
    The main one is create_df_tx which load all the transactions from the csv files
    """

    def __init__(self, path_to_transaction_folder):
        """
        Initialize the class with the path to the folder containing the csv files as exported by Flipside package
        It should contain a folder for each chain (ethereum, arbitrum, polygon, etc.) and inside are the csv files name
        as eoa_tx.csv
        Parameters
        ----------
        path_to_transaction_folder : str
            The path to the folder containing the csv files
        """
        self.path_to_tx_dir = path_to_transaction_folder

    def create_df_all_transactions(self, files, tx_chain, n_files=-1):
        """
        Create a dataframe with all transactions from a given chain.
        Parameters
        ----------
        files : list
            A list of files to load
        tx_chain : str
            The chain to load the transactions from. For example "ethereum"
        n_files : int
            The number of files to load. If -1, all files are loaded

        Returns
        -------
        df : pd.DataFrame
            A dataframe with all transactions from the given chain

        """
        if n_files == -1:
            df_list = [self.load_df_transactions(files[f_i], tx_chain) for f_i in range(len(files))]
        else:
            df_list = [self.load_df_transactions(files[f_i], tx_chain) for f_i in range(n_files)]
        df = pd.concat(df_list)
        return df

    @staticmethod
    def get_files(path, chain):
        """
        Get the list of files in a given path and chain
        Parameters
        ----------
        path : str
            The path to the folder containing the network folder
        chain : str
            The name of the chain to list the files of

        Returns
        -------
        files : list
            A list of files in the given path and chain
        """
        path_to_csv = os.path.join(path, chain)
        files = os.listdir(path_to_csv)
        return files

    def get_files_in_address(self, chain, address_list):
        """
        Get the list of files in a given path and chain and that are in the address list
        Parameters
        ----------
        chain : str
            The name of the chain to list the files of
        address_list : list
            A list of addresses to filter the contributors

        Returns
        -------
        files : list
            A list of files in the given path and chain and filtered by the address list

        """
        all_files = self.get_files(self.path_to_tx_dir, chain)
        files = [file for file in all_files if self.get_address_name(file) in address_list]
        return files

    def create_df_tx(self, tx_chain, address_list=None, n_files=-1):
        """
        Create a dataframe with all transactions from a given chain.
        You can provide a list of addresses to filter the contributors. For example if you want to study the sybil of a
        given grant or project

        Parameters
        ----------
        tx_chain : str
            The chain to study. For example "ethereum"
        address_list : list
            A list of addresses to filter the contributors
        n_files : int
            The number of files to load. If -1, all files are loaded

        Returns
        -------
        df : pd.DataFrame
            A dataframe with all transactions from the given chain

        """

        if address_list is None:
            files = self.get_files(self.path_to_tx_dir, tx_chain)
        else:
            files = self.get_files_in_address(tx_chain, address_list)

        if n_files == -1:
            df_list = [self.load_df_tx(files[f_i], tx_chain) for f_i in range(len(files))]
        else:
            df_list = [self.load_df_tx(files[f_i], tx_chain) for f_i in range(n_files)]
        df = pd.concat(df_list)
        return df

    def load_df_tx(self, file_name, tx_chain):
        """
        Load a dataframe with all transactions from a given file name and chain
        Parameters
        ----------
        file_name : str
            The name of the file to load
        tx_chain : str
            The chain to load the transactions from. For example "ethereum"

        Returns
        -------
        df : pd.DataFrame
            A dataframe with all transactions from the given file name and chain
            Adds a column with the EOA name

        """
        path_dir = os.path.join(self.path_to_tx_dir, tx_chain)
        full_path = os.path.join(path_dir, file_name)
        try:
            df = pd.read_csv(full_path)
        except Exception as e:
            print(e)
            print("Error reading file: {}".format(full_path))
            raise
        if not "EOA" in df.columns.values:
            df["EOA"] = self.get_address_name(file_name)
        return df

    @staticmethod
    def get_address_name(file_name):
        """return the address name from the file name"""
        return file_name.split('_')[0]
