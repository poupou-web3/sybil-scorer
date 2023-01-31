import os
import sys
from pathlib import Path

import pandas as pd
from sbdata.FlipsideApi import FlipsideApi

absolute_path = os.fspath(Path.cwd().parent.parent)
if absolute_path not in sys.path:
    sys.path.append(absolute_path)

# set the api key using the environment variable
api_key = os.environ['FLIPSIDE_API_KEY']

# initialize the flipside api
flipside_api = FlipsideApi(api_key, max_address=1000)

# set the path to the address file and the path to export the transactions
PATH_TO_ADDRESS = "../../data/grants/df_contribution_address_OSS.csv"
PATH_TO_EXPORT = "../../data/transactions/OSS"

# read the contributor address from oss grant and convert to a list
df_address = pd.read_csv(PATH_TO_ADDRESS)
list_unique_address = df_address.address.unique()

print("Start mining transactions")
# to export all transactions from the supported chains
flipside_api.extract_transactions(PATH_TO_EXPORT, list_unique_address)

# to export all transactions from a specific chain here with ethereum
# flipside_api.extract_transactions_net(PATH_TO_EXPORT, list_unique_address, 'ethereum')

print("End mining transactions")
