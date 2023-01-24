# cluster-scorer

## Installation
download data in https://huggingface.co/datasets/Poupou/Gitcoin-Grant-DataBuilder/tree/main

extract zip to have 
"data/grants" folder at the root of the folder

Then run the jupyter notebook jupyter/normalize_contribution_data.ipynb
this will create files in grants folder

Then run file [extract_all_txs.py](https://github.com/poupou-web3/cluster-scorer/blob/main/src/main/extract_all_txs.py) 
this will take a lot of time (not sure it is working yet)

update: some address have so many transactions that the query time out, seting batching by 50 addresses or less should help fix that
Another way could be to create a new query that retrieve all transactions from all chain for one address. and then export that to csv named with the _address_transactions.csv

The issue is that there are more than 75 000 address to query and only 10 000 API call per rolling day.


and then [extract_tags_labels.py](https://github.com/poupou-web3/cluster-scorer/blob/main/src/main/extract_tags_labels.py)
this retrieves tags and labels for all addresses found in the transactions folder (not working to many addresses in unique_address WIP)

## Specifications
[Spec.md](https://github.com/poupou-web3/cluster-scorer/blob/main/spec.md) describes which legos we should build

## Lego example 
https://github.com/Fraud-Detection-and-Defense/lego-docs

## Folder details
Jupyter folder holds notebooks for data cleaning and data exploration

src/main has many things I built in the previous hackhathon
- features
- plot
- utils
-extract_etherscan
- extract polygon

these are methods and scripts that I used to extract data using etherscan and polygon scan they should be removed but may be useful. Especially for tsfresh lego we should reuse code I did in features and utils

the Flipside repo holds the class that allows to query the FlipsideAPI. It is still in dev.


tree .\reader-whl\ /F