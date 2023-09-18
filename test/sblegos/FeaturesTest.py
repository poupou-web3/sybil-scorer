import os
import unittest
from pathlib import Path

import pandas as pd

from sbscorer.sblegos.FeatureCreator import FeatureCreator
from sbscorer.sbutils.LoadData import LoadData


class FeaturesTest(unittest.TestCase):
    current_dir = Path(os.getcwd())
    path_to_resources = os.path.join(current_dir.parent, "resources")
    path_to_tx = os.path.join(path_to_resources, "transactions")
    dataLoader = LoadData(path_to_tx)
    path_to_test_add = os.path.join(path_to_resources, "test_address")

    df_address = pd.read_csv(os.path.join(path_to_test_add, "tx_analyser_address.csv"))
    df_tx = dataLoader.create_df_tx("ethereum")
    df_tx.rename(columns={"EOA": "eoa", "eth_value": "value"}, inplace=True)
    df_tx["block_number"] = 0

    fc = FeatureCreator(df_tx)

    def test_get_features(self):
        df_features = self.fc.create_feature_df()
        self.assertEqual(df_features.shape[0], 3)


if __name__ == '__main__':
    unittest.main()
