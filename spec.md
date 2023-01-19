# Specifications

## Goal

Create legos for sybil defense

## Idea 

Either 
- create one package that takes in inputs df_application_normalized and df_contributions_normalized, retrieved the required data and run lego algorithm 
- create two package one that retrives the data we need and another that contains all the algorithm with input the output of the first package

## Data retrieval lego
The lego takes as input a list of unique addresses (contributors to grants) extracted from df_contributions_normalized.
It creates a data folder, inside are extracted all the transactions on various chains (ethereum, polygon, arbitrum, optimism, gnosis, avalanche) 
more network later on based on additions from flipside crypto to fact_transaction tables
It queries flipside crypto to get all transactions that have happened for an address


Then the script also retrieves labels and tags for any address from the addresses found in the transactions


## Algorithm Legos

### 1. Seed wallet 
This lego analysed the first transaction received by an address also called "seed" 
because it is the transaction that then allows the user to perform actions on the blockchain.

Input:
- 1 address
- Grant round and project_id
- Data folder 
  - Transactions
  - Contributions
  - Applications

Output:
- boolean is_suspicious_seed (if the address was funded by an address that is reoccuring as seeding in the round/project)



### 2. Transaction similitude
This lego analysed the behavior of all the transactions performed by an address and compare it to all the contributors of the grant.


Input:
- 1 address
- Grant round and project_id
- Data folder 
  - Transactions
  - Contributions
  - Applications

Output:
- boolean has_similitude_address 



### 3. Contribution 
This lego analysed the behavior of all the contributions performed by an address.


Input:
- 1 address
- Grant round and project_id
- Data folder 
  - Contributions
  - Applications

Output:
- boolean has_only_one_contribution_on_project
- boolean first_contribution
- boolean contributed multiple times on project
- boolean contributed_multiple_times_on_other_project


### 3. TSFRESH 
This lego analysed the behavior of the transactions performed by an address by using tsfresh and kmean


Input:
- 1 address
- Data folder 
  - Transactions

Eventually it could use the data from the grant to know which address has participated in the grant/project

Output:
- rank sybil score


