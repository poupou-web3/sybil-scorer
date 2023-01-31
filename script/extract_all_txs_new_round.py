import os
import sys
from pathlib import Path

import pandas as pd

absolute_path = os.fspath(Path.cwd().parent)
if absolute_path not in sys.path:
    sys.path.append(absolute_path)

from sbscorer.sbdata.FlipsideApi import FlipsideApi

api_key = os.environ['FLIPSIDE_API_KEY']

PATH_TO_ADDRESS = "../data/grants/df_new_grant_contributor_address.csv"
PATH_TO_EXPORT = "../data/transactions_alpha_round"

df_address = pd.read_csv(PATH_TO_ADDRESS)
list_unique_address = df_address.address.unique()

flipside_api = FlipsideApi(api_key, max_address=1000)
flipside_api.extract_transactions(PATH_TO_EXPORT, list_unique_address)

print("End mining transactions")
