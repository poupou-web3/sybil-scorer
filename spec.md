# Specifications

## Goal

Create legos for sybil defense

## Idea 

Either 
- create one package that takes in inputs df_application_normalized and df_contributions_normalized, retrieved the required data and run lego algorithm 
- create two package one that retrives the data we need and another that contains all the algorithm with input the output of the first package




## Requirements:

### [Outputs](https://github.com/Fraud-Detection-and-Defense/lego-docs#outputs)
```
The Lego should output one or both of:

a Boolean: representing Sybil or non-Sybil as predicted by the Lego
1 = Sybil, 0 = non-Sybil
a float: representing the Sybil likelihood or "trust score" as predicted by the Lego.
higher score = greater likelihood of being Sybil (trust = 1-score)
```
### Docker?
 https://github.com/Fraud-Detection-and-Defense/lego-docs#containerization

I've never used before so may be otpionnal first espscially it is not needed if we package in a pipy package

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


## [Lego ideas extracted from FDD](https://github.com/Fraud-Detection-and-Defense/lego-docs#lego-ideas)

During Season 14, Gitcoin Passport was integrated into Bankless Academy. Analysis revealed that Gitcoin Passport was most powerful when combined with additional anti-Sybil Legos.

- **Farmer Boolean**: (uses on-chain data to determine whether a user has >X ERC-20 tokens and an average transaction value <Y ETH)
- **Onchain History Boolean**: (has a user engaged in certain web3 activities in a specific timeframe? Activites and timeframe can be customized by round owner)
- **Money-Mixer**: (Does a user interact with mixers e.g. Tornado cash)
- **On-Trend / Off-Trend**: (is the donation profile of a user similar to a grant’s target community?)
- **Flagged Activity on Etherscan**: (is an address closely associated with addresses flagged as phishing/spam on etherscan?)


Other simple Legos could be checks for users that hold certain POAPs or NFTs. Some POAPs and NFTs are easy to farm, others require significant investment of time and/or capital. For example, some education programs award their graduates NFTs as proof of completion - those are difficult to farm without taking a course, and they are in very limited supply so the total bribable population is small - ownership of these credentials is good evidence a user is not a Sybil attacker.


Not all Legos have to use on-chain data. There may be more Sybil signals that can be extracted using clever analysis of Gitcoin data - DonorDNA and GrantDNA are good examples of existing Legos that only use off-chain data.



