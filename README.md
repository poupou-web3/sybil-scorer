# cluster-scorer

download data in https://huggingface.co/datasets/Poupou/Gitcoin-Grant-DataBuilder/tree/main

extract zip to have 
"data/grants" folder at the root of the folder

Then run the jupyter notebook jupyter/normalize_contribution_data.ipynb
this will create files in grants folder

Then run file [extract_all_txs.py](https://github.com/poupou-web3/cluster-scorer/blob/main/src/main/extract_all_txs.py) 
this will take a lot of time (not sure it is working yet)


and then [extract_tags_labels.py](https://github.com/poupou-web3/cluster-scorer/blob/main/src/main/extract_tags_labels.py)
this retrieves tags and labels for all addresses found in the transactions folder
