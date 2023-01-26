import os

import pandas as pd


class LoadData(object):

    def __init__(self, path_to_transaction_folder):
        self.path_to_tx_dir = path_to_transaction_folder

    def create_df_all_transactions(self, files, tx_chain, n_files=-1):
        if n_files == -1:
            df_list = [self.load_df_transactions(files[f_i], tx_chain) for f_i in range(len(files))]
        else:
            df_list = [self.load_df_transactions(files[f_i], tx_chain) for f_i in range(n_files)]
        df = pd.concat(df_list)
        return df

    @staticmethod
    def load_df_transactions(param, tx_chain):
        pass

    @staticmethod
    def get_files(path, chain):
        path_to_csv = os.path.join(path, chain)
        files = os.listdir(path_to_csv)
        return files

    def get_files_in_address(self, chain, address_list):
        all_files = self.get_files(self.path_to_tx_dir, chain)
        files = [file for file in all_files if self.get_address_name(file) in address_list]
        return files

    def create_df_tx(self, tx_chain, address_list=None, n_files=-1):

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
        return file_name.split('_')[0]
