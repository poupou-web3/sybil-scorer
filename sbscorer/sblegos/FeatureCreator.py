from tsfresh.feature_extraction import extract_features
from tsfresh.utilities.dataframe_functions import impute

from sbscorer.sblegos.Transaction import Transaction
from sbscorer.sblegos.features.conf import FC_TSFRESH_VALUE, FC_TSFRESH_TIME, FC_TSFRESH_GAS_2
from sbscorer.sblegos.features.create_features import get_df_interact_stats

ETH_DECIMAL = 10E18


class FeatureCreator(Transaction):

    def __init__(self, df_transactions, array_address=None):
        super().__init__(df_transactions, array_address)

        self.df_transactions.sort_values("block_timestamp", inplace=True)  # required by tsfresh
        self.df_transactions.reset_index(drop=True, inplace=True)
        self.df_transactions.reset_index(inplace=True)
        self.df_transactions["value"] = self.df_transactions["value"].apply(lambda x: float(x) / ETH_DECIMAL)

    def create_feature_df(self):
        df_extract_from_v = self.df_transactions.loc[:, ["index", "eoa", "value"]]
        # extract features with tsfresh
        features_tsfresh_v = extract_features(df_extract_from_v,
                                              column_id='eoa',
                                              column_sort='index',
                                              default_fc_parameters=FC_TSFRESH_VALUE,
                                              # we impute = remove all NaN features automatically
                                              impute_function=impute)
        features_tsfresh_v.reset_index(inplace=True)

        df_extract_from_t = self.df_transactions.loc[:, ["index", "eoa", "block_timestamp"]]
        # extract features with tsfresh
        features_tsfresh_t = extract_features(df_extract_from_t,
                                              column_id='eoa',
                                              column_sort='index',
                                              default_fc_parameters=FC_TSFRESH_TIME,
                                              # we impute = remove all NaN features automatically
                                              impute_function=impute)
        features_tsfresh_t.reset_index(inplace=True)

        df_extract_from_gas = self.df_transactions.loc[:, ["index", "eoa", "gas_used", "gas_limit"]]
        # extract features with tsfresh
        features_tsfresh_gas = extract_features(df_extract_from_gas,
                                                column_id='eoa',
                                                column_sort='index',
                                                kind_to_fc_parameters=FC_TSFRESH_GAS_2,
                                                # we impute = remove all NaN features automatically
                                                impute_function=impute)
        features_tsfresh_gas.reset_index(inplace=True)

        features_interact = get_df_interact_stats(self.df_transactions)

        merge1 = features_interact.merge(features_tsfresh_gas, left_on="address", right_on="index",
                                         validate="one_to_one").drop(columns=["index"])
        merge1 = merge1.merge(features_tsfresh_t, left_on="address", right_on="index", validate="one_to_one").drop(
            columns=["index"])
        merge1 = merge1.merge(features_tsfresh_v, left_on="address", right_on="index", validate="one_to_one").drop(
            columns=["index"])
