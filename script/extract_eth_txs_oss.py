import pandas as pd
import sys
import os
from pathlib import Path

absolute_path = os.fspath(Path.cwd().parent.parent)
if absolute_path not in sys.path:
    sys.path.append(absolute_path)

from sbscorer.flipside.FlipsideApi import FlipsideApi

# read the address from oss grant

api_key = os.environ['FLIPSIDE_API_KEY']
flipside_api = FlipsideApi(api_key, max_address=50)
PATH_TO_ADDRESS = "../../data/grants/df_contribution_normalized_OSS.csv"
PATH_TO_EXPORT = "../../data/transactions/OSS"

df_address = pd.read_csv(PATH_TO_ADDRESS)
list_unique_address = df_address.address.unique()

flipside_api.extract_transactions(PATH_TO_EXPORT, list_unique_address)
# flipside_api.extract_transactions_net(PATH_TO_EXPORT, list_unique_address, 'ethereum')
# flipside_api.extract_transactions_net(PATH_TO_EXPORT, list_unique_address, 'polygon')
# flipside_api.extract_transactions_net(PATH_TO_EXPORT, list_unique_address, 'avalanche')
# flipside_api.extract_transactions_net(PATH_TO_EXPORT, list_unique_address, 'optimism')
# flipside_api.extract_transactions_net(PATH_TO_EXPORT, list_unique_address, 'gnosis')
# flipside_api.extract_transactions_net(PATH_TO_EXPORT, list_unique_address, 'arbitrum')

print("End mining transactions")
