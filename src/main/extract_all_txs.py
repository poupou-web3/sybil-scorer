import pandas as pd
import sys
import os
from pathlib import Path

absolute_path = os.fspath(Path.cwd().parent.parent)
if absolute_path not in sys.path:
    sys.path.append(absolute_path)

from src.main.flipside.FlipsideApi import FlipsideApi


api_key = os.environ['FLIPSIDE_API_KEY']
flipside_api = FlipsideApi(api_key)
PATH_TO_ADDRESS = "../../data/grants/unique_ctbt_address.csv"
PATH_TO_EXPORT = "../../data/transactions"

df_address = pd.read_csv(PATH_TO_ADDRESS)
list_unique_address = df_address.address.unique()

flipside_api.extract_transactions(PATH_TO_EXPORT, list_unique_address)

print("End mining transactions")
