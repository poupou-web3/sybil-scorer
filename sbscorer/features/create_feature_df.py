import sys
import os
from pathlib import Path
absolute_path = os.fspath(Path.cwd().parent)
if absolute_path not in sys.path:
    sys.path.append(absolute_path)

import pandas as pd
import numpy as np
import os

from sbscorer.features.conf import FC_TSFRESH
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import impute

from sbscorer.utils.processing import *
from sbscorer.features.conf import *
from sbscorer.features.create_features import *

N_FILES = -1
ETH_DECIMAL = 10E18

tx_chain = 'eth_std' # change the chain to "eth_polygon" if you wish to create features for polygon chain 
RELATIVE_PATH_TX = '/data/transactions/'

if __name__ == '__main__':
        
    path_to_data = absolute_path + RELATIVE_PATH_TX + tx_chain
    path_to_data = get_path_to_data(absolute_path, tx_chain)
    files = get_files(absolute_path, tx_chain)

    df = create_df_all_transactions(path_to_data, files, tx_chain, n_files=N_FILES)

    # transactions are sorting in descending order of time stamp
    # to use extract_features we must sort in ascending order
    df.sort_values("timeStamp", inplace=True)

    # reset index two times to reinitialise the order(to ascending sort) to use it as a time serie indexer 
    df = df.reset_index(drop=True).reset_index()

    # convert value column to float and 
    df["value"] = [float(df.loc[i, "value"])/ETH_DECIMAL for i in range (df.shape[0])]

    # df["gas"] = df.loc[:, "gas"]/10E18
    # df["gasPrice"] = df.loc[:, "gasPrice"]/10E18

    print(df.shape)

    # df_extract_from = df.loc[:,["index", "address", "timeStamp", "value", "gas","gasPrice"]]
    # #extract features with tsfresh
    # features_tsfresh = extract_features(df_extract_from,
    #                     column_id='address',
    #                     column_sort='index',
    #                     kind_to_fc_parameters=FC_TSFRESH,
    #                     # we impute = remove all NaN features automatically
    #                     impute_function=impute)
    # features_tsfresh.reset_index(inplace=True)

    df_extract_from_v = df.loc[:,["index", "address", "value"]]
    #extract features with tsfresh
    features_tsfresh_v = extract_features(df_extract_from_v,
                        column_id='address',
                        column_sort='index',
                        default_fc_parameters=FC_TSFRESH_VALUE,
                        # we impute = remove all NaN features automatically
                        impute_function=impute)
    features_tsfresh_v.reset_index(inplace=True)

    df_extract_from_t = df.loc[:,["index", "address", "timeStamp"]]
    #extract features with tsfresh
    features_tsfresh_t = extract_features(df_extract_from_t,
                        column_id='address',
                        column_sort='index',
                        default_fc_parameters=FC_TSFRESH_TIME,
                        # we impute = remove all NaN features automatically
                        impute_function=impute)
    features_tsfresh_t.reset_index(inplace=True)

    df_extract_from_gas = df.loc[:,["index", "address", "gas", "gasPrice"]]
    #extract features with tsfresh
    features_tsfresh_gas = extract_features(df_extract_from_gas,
                        column_id='address',
                        column_sort='index',
                        kind_to_fc_parameters=FC_TSFRESH_GAS_2,
                        # we impute = remove all NaN features automatically
                        impute_function=impute)
    features_tsfresh_gas.reset_index(inplace=True)

    features_interact = get_df_interact_stats(df)

    merge1 = features_interact.merge(features_tsfresh_gas, left_on="address", right_on="index", validate="one_to_one").drop(columns=["index"])
    merge1 = merge1.merge(features_tsfresh_t, left_on="address", right_on="index", validate="one_to_one").drop(columns=["index"])
    merge1 = merge1.merge(features_tsfresh_v, left_on="address", right_on="index", validate="one_to_one").drop(columns=["index"])

    if N_FILES != -1:
        assert merge1.shape[0] == N_FILES

    path_to_features_export = os.path.join(absolute_path, "data")
    path_to_features_export = os.path.join(path_to_features_export, "features")
    path_to_features_export = os.path.join(path_to_features_export, tx_chain)
    
    if not os.path.exists(path_to_features_export):
        os.makedirs(path_to_features_export)
    csv_name ="features_" + tx_chain + ".csv"
    path_to_features_export = os.path.join(path_to_features_export, csv_name)
    merge1.to_csv(path_to_features_export, index=False)





