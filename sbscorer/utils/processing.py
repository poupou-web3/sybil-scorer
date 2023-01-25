import os
import pandas as pd

RELATIVE_PATH_TX = '/data/transactions/'

def get_path_to_data(absolute_path, tx_chain):
    return absolute_path + RELATIVE_PATH_TX + tx_chain


def get_files(absolute_path, tx_chain):
    relative_path_to_data = RELATIVE_PATH_TX + tx_chain 
    path_to_data = absolute_path + relative_path_to_data
    files = os.listdir(path_to_data)
    return files


def get_address_name(file_name, tx_chain):
    return file_name.replace(tx_chain, '').split('_')[1]


def load_df_transactions(path_to_data, file, tx_chain):
    df = pd.read_csv(os.path.join(path_to_data, file), index_col=0)
    if not "address" in df.columns.values:
        df["address"] = get_address_name(file, tx_chain)
    return df


def create_df_all_transactions(path_to_data, files, tx_chain, n_files=-1):
    if n_files == -1:
        df_list = [load_df_transactions(path_to_data, files[f_i], tx_chain) for f_i in range (len(files))]
    else:
        df_list = [load_df_transactions(path_to_data, files[f_i], tx_chain) for f_i in range (n_files)]
    df = pd.concat(df_list)
    return df


def save_csv(df, data_dir, csv_name, network):
    csv_dir = os.path.join(data_dir, network)
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    csv_path = os.path.join(csv_dir, csv_name)
    df.to_csv(csv_path, index=False)

        