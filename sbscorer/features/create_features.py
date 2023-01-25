import pandas as pd
import numpy as np


def get_n_outgoing_tx(df, address):
    return (df['from'] == address).sum()


def get_r_out_tx(df, address):
    return get_n_outgoing_tx(df, address) / df.shape[0]


def get_distinct_address_interact(df):
    return len(np.unique(np.append(df['from'].values, df['to'].values))) - 1


# return a df with address and countTx columns, the number of transactions
def get_df_count_tx(df):
    df_tx = df[["hash", "address"]].groupby(by="address").count().reset_index()
    return df_tx.set_axis(["address", "countTx"], axis=1)

def get_df_outgoing_tx(df):
    # number of outgoing transactions
    df_m = df[["outgoing", "address"]].groupby(by="address").sum().reset_index()
    return df_m

def get_df_outgoing_tx_ratio(df):
    # ratio of outgoing transactions
    df_m = df[["outgoing", "address"]].groupby(by="address").apply(lambda x: x.sum()/ x.count()).reset_index().set_axis(["address", "outgoingRatio"], axis=1)
    return df_m

def get_df_interaction(df):
    # unique address interactions
    df_interacted = pd.concat([df.loc[:,["address", "from"]].set_axis(["address", "interacted"], axis=1), df.loc[:,["address", "to"]].set_axis(["address", "interacted"], axis=1)], join="inner")
    unique_interacted = df_interacted.groupby(by="address")["interacted"].unique()
    df_unique_interacted = pd.DataFrame(unique_interacted).reset_index()
    df_unique_interacted["countUniqueInteracted"] = np.nan
    df_unique_interacted["ratioUniqueInteracted"] = np.nan

    for i_address in range (df_unique_interacted.shape[0]):
        unique_interaction = len(df_unique_interacted.loc[i_address, "interacted"]) - 1
        df_unique_interacted.loc[i_address, "countUniqueInteracted"] = unique_interaction

    df_unique_interacted.drop(columns=["interacted"], inplace=True)
    
    return df_unique_interacted


def get_df_interact_stats(df):

    df_unique_interacted = get_df_interaction(df)
    df_count_tx = get_df_count_tx(df)

    df_interact = df_unique_interacted.merge(df_count_tx, on="address", validate="one_to_one")
    df_interact["ratioUniqueInteracted"] = df_interact["countUniqueInteracted"] / df_interact["countTx"]

    df["outgoing"] = df["address"] == df["from"]
    df_outgoing_tx = get_df_outgoing_tx(df)
    df_interact = df_interact.merge(df_outgoing_tx, on="address", validate="one_to_one")

    df_outgoing_tx_ratio = get_df_outgoing_tx_ratio(df)
    df_interact = df_interact.merge(df_outgoing_tx_ratio, on="address", validate="one_to_one")

    return df_interact