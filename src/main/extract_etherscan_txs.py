import pandas as pd

import sys
import os
from pathlib import Path
absolute_path = os.fspath(Path.cwd().parent)
if absolute_path not in sys.path:
    sys.path.append(absolute_path)
print(sys.path)
from src.main.utils.MineEthTx import MineEthTx


API_KEY = '1NAV5EVGAV9S7ZJIKP586RT8U1X4CWDSJ3'
PER_PAGE = 100
TX_CHAIN ='eth_std'

from_address_nbr = 15126
to_address_nbr = 200000


miner = MineEthTx(API_KEY, PER_PAGE, 0)

df_contrib = pd.read_csv(absolute_path + '/data/hackathon-contributions-dataset_v2.csv')


df_eth_std = df_contrib[df_contrib['chain'] == TX_CHAIN]
unique_eth_std_address = df_eth_std['address'].unique()
print("Unique eth adresses :" + str(unique_eth_std_address))

path_to_export = absolute_path + '/data/transactions/' + TX_CHAIN

full_path_to_logs = absolute_path + '/logs/log_' + TX_CHAIN + ".txt"
f = open(full_path_to_logs, "a")

for ads in unique_eth_std_address[from_address_nbr : min(to_address_nbr, len(unique_eth_std_address) + 1)]:
    f.write('Address'+ ' #' + str(from_address_nbr) + ' ' + ads + 'api call #' + str(miner.api_counter) + '\n')
    print('Address'+ ' #' + str(from_address_nbr) + ' ' + ads + 'api call #' + str(miner.api_counter))
    miner.create_csv(path_to_export, ads, 'normal', TX_CHAIN)
    from_address_nbr += 1

f.close()

print("End mining ethereum transactions")
