# sybil-scorer

Sybil scorer is a python package that provides useful classes and methods to analyze the behavior of addresses.

## Help Out
Consider donating on Gitcoin [https://explorer.gitcoin.co/#/round/10/0x8de918f0163b2021839a8d84954dd7e8e151326d/0x8de918f0163b2021839a8d84954dd7e8e151326d-66](https://explorer.gitcoin.co/#/round/10/0x8de918f0163b2021839a8d84954dd7e8e151326d/0x8de918f0163b2021839a8d84954dd7e8e151326d-66)

## Installation

- Python >= 3.9
- ```pip install sybil-scorer```

## What is inside?

The package has two main sub-packages.

- **sbdata** is a package to easily retrieve a large amount of data from the Flipside API.
- **sblegos** a package to perform on-chain transactions analysis to detect potential Sybil behavior.
- **sbutils** is a package that makes it easy to load the data extracted with sbdata and use it in sblegos.

More details on the packages and examples are provided below.

### sbdata

An example script to retrieve data from the flipside API is provided in the script folder:
script/demo_extract_eth_txs_oss.py

It could also be used to retrieve transactional data from an address with some simple calls:

``` python
import os
from sbdata.FlipsideApi import FlipsideApi

api_key = os.environ['FLIPSIDE_API_KEY']
flipside_api = FlipsideApi(api_key, max_address=1000)
address = ['0x06cd8288dc001024ce0a1cf39caaedc0e2db9c82']
tx_add_eth = flipside_api.get_transactions(address, chain='ethereum')
```

It walks you through the process of retrieving data from the flipside API and saving it in a folder.

To use this package you will need an API key from flipside that you can get
here: https://sdk.flipsidecrypto.xyz/shroomdk/apikeys

Useful example script are provided in the script folder.

### sblegos and sbutils

sblegos provides the following analysis of legos:

- **has_same_seed** : true if the address has the same seed as any other address in the grants contributors
- **has_same_seed_naive** : true if the address has the same seed as any other address in the grants contributors with a
  naive approach: address of the from_address of the first transaction.
- **has_suspicious_seed_behavior** : true if has_same_seed is different from has_same_seed_naive. It means the user
  performed some actions before funding his wallet.
- **has_interacted_with_other_contributor** : true if the user has interacted with any other contributor to the grant
- **has_less_than_n_transactions** : true if the user has less than n transactions.
- **has_transaction_similitude** : true if the user has a transaction history that is similar to any other contributor
  to the grant.
- **has_transaction_similitude_opti** : an optimized version of has_transaction_similitude, when used across multiple
  addresses.

A jupyter notebook using both packages is available as a jupyter notebook
here https://github.com/poupou-web3/grant-exploration/blob/main/gr-climate-exploration.ipynb

The following snippet of code will check if any address has the same seed as any other contributor to the climate grant

``` python
import os
from pathlib import Path
import numpy as np
import pandas as pd
from sbutils import LoadData
from sblegos.TransactionAnalyser import TransactionAnalyser as txa

# Set path to data folder
PATH_TO_EXPORT = 'path to where the data was extracted'
CHAIN = 'the name of the chain you want to analyse for example "ethereum"'

# Load the votes data
array_unique_address = df_votes['voter'].unique() # array of unique voters, here df_votes contains all the votes made on a grant 

# Be sure that the address are in lower case
array_unique_address = np.char.lower(array_unique_address.astype(str))
print(f'Number of unique voter: {len(array_unique_address)}')

# Load the transactions of the addresses using the sbutils package
data_loader = LoadData.LoadData(PATH_TO_EXPORT)
df_tx = data_loader.create_df_tx(CHAIN, array_unique_address)

# Initialise the TransactionAnalyser class
tx_analyser = txa(df_tx, array_address=array_unique_address)

# Compute some predetermined features, it can takes some time especially on large datasets
df_matching_address = tx_analyser.get_df_features()
df_matching_address.head(2)

# For individual computation of the features:
df_matching_address = pd.DataFrame(array_unique_address, columns=["address"])
df_matching_address['seed_same_naive'] = df_matching_address.loc[:, 'address'].apply(lambda x : tx_analyser.has_same_seed_naive(x))

```

## Documentation

The documentation of the package is available at https://sybil-scorer.readthedocs.io/en/latest/py-modindex.html.
For a local version of the documentation, you can build it using sphinx. with the following commands:

```
cd docs
sphinx-apidoc -o ./source ../sbscorer
make html
```

Then open the file docs/build/html/index.html in your browser.
The local version of the documentation is prettier than the one hosted on readthedocs.
![doc.png](img/doc.png)

## Example Data

Some data for easier use of the package in the context of Gitcoin grants are made available on Ocean market.

### Gitcoin Citizen Round data

#### Transaction data

You can load the data directly into the `df_tx` variable.
https://huggingface.co/datasets/Poupou/Gitcoin-Citizen-Round/blob/main/tx_citizen_round.parquet

These are all the transactions performed by users who contributed to the Citizen round on grant as of 30th of June 2023.

#### Example of vote data

Example query to extract the vote data of the citizen round of June 2023 from the Flipside API:
https://flipsidecrypto.xyz/poupou/q/j3E9SEfMLkxG/citizen-round-votes

You could also use the data available on hugging face:
https://huggingface.co/datasets/Poupou/Gitcoin-Citizen-Round/blob/main/citizen-votes.csv

## Future works

Future works include:

- Adding more transactional analysis lego.
- Adding temporal features to a clustering algorithm as researched in the first
  hackathon [submission](https://github.com/poupou-web3/GC-ODS-Sybil).
- Improving seed legos to output cluster of addresses instead of a boolean.
- See issues at www.github.com/poupou-web3/sybil-scorer/issues
