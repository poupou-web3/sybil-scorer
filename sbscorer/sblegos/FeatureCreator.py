import pandas as pd
from tsfresh.feature_extraction import extract_features
from tsfresh.utilities.dataframe_functions import impute

from sbscorer.sblegos.Transaction import Transaction
from sbscorer.sblegos.features.conf import FC_TSFRESH

ETH_DECIMAL = 10E18


class FeatureCreator(Transaction):

    def __init__(self, df_transactions, array_address=None):
        super().__init__(df_transactions, array_address)

        self.df_transactions.sort_values("block_timestamp", inplace=True)  # required by tsfresh
        self.df_transactions.reset_index(drop=True, inplace=True)
        self.df_transactions.reset_index(inplace=True)
        self.df_transactions.rename(columns={"index": "index_tx"}, inplace=True)
        self.df_transactions["value"] = self.df_transactions["value"].apply(lambda x: float(x) / ETH_DECIMAL)

    def create_feature_df(self):
        df_features = self.df_transactions[
            ['index_tx', 'eoa', 'block_timestamp', 'value', 'tx_fee', 'gas_used', 'gas_limit']]

        df_features['block_timestamp'] = (pd.to_datetime(df_features["block_timestamp"])).astype('int64') // 10E9
        features_tsfresh = extract_features(df_features,
                                            column_id='eoa',
                                            column_sort='index_tx',
                                            kind_to_fc_parameters=FC_TSFRESH,
                                            # we impute = remove all NaN features automatically
                                            impute_function=impute)
        features_tsfresh.reset_index(inplace=True)
        features_tsfresh.rename(columns={"index": "eoa"}, inplace=True)

        return features_tsfresh
