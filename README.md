# sybil-scorer

## What is it?
Sybil scorer is a python package that provides useful classes and method to analyse the behaviour of addresses. 


## Installation

Pip install sybil-scorer

## What should I use?

The package has two main sub-packages. 
- flipside a package to easily retrieve large amount of data from he flipside API. 
- legos a package to perform on chain transactions analysis. Currently the methods are made to easily detect Sybil behaviour. 

## Additional Data 

Some data for an easier use of the package in the context of Gitcoin grants are made available at :
https://huggingface.co/datasets/Poupou/Gitcoin-Grant-DataBuilder/tree/main

### Ethereum Transaction Data
Ethereum Transaction data are available for download on Ocean here:

These are all the transactions performed by users who contributed to the grant as of 20th of January 2022.
It is organised with one csv file for each address to facilitate the loading of only the necessary data transactions when performing analysis on a specific grant or project. 
The data was produced using the flipside package. 

### Grant Data and Addresses 
The data provided by Gitcoin was standardised in the same format for all grants to make it easier to manipulate and find the desired wallet addresses of contributors to a specific project for example. 

These can be recreated by using the files provided by ODC/Gitcoin and running the Jupyter notebook in the Jupyter folder. 
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
