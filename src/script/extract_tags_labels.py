import pandas as pd
import numpy as np
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
PATH_TO_TRANSACTIONS = "../../data/transactions"
PATH_TO_TAGS = "../../data/tags"

# Extract transactions from all csv in PATH_TO_TRANSACTIONS
list_address = []
for network in os.listdir(PATH_TO_TRANSACTIONS):
    print("Extracting transactions for network: ", network)
    path_to_export = os.path.join(PATH_TO_TRANSACTIONS, network)
    for file in os.listdir(path_to_export):
        df_address = pd.read_csv(
            os.path.join(path_to_export, file),
            usecols=["from_address", "to_address"])
        list_address.append(df_address.from_address.values)
        list_address.append(df_address.to_address.values)

list_address = np.concatenate(list_address)
list_unique_address = np.unique(list_address.astype(str))

print("Start extracting tags")
sql_tag = flipside_api.get_all_cross_chain_info_sql_query(info_type="tag", list_unique_address)
df_tags = flipside_api.execute_query(sql_tag)
print("End extracting tags")

print("Start extracting labels")
sql_labels = flipside_api.get_all_cross_chain_info_sql_query(info_type="label", list_unique_address)
df_labels = flipside_api.execute_query(sql_labels)
print("End extracting labels")

print("export_to_csv")

if not os.path.exists(PATH_TO_TAGS):
    os.makedirs(PATH_TO_TAGS)

df_tags.to_csv(os.path.join(PATH_TO_TAGS, "tags.csv"), index=True)
df_labels.to_csv(os.path.join(PATH_TO_TAGS, "labels.csv"), index=True)

print("End")
