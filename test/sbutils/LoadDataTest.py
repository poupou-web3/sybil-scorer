import unittest

from sbscorer.sbutils.LoadData import LoadData


class LoadDataTest(unittest.TestCase):
    path_to_tx = "../resources/transactions"
    dataLoader = LoadData(path_to_tx)

    def test_get_files(self):
        chain = "ethereum"
        files = self.dataLoader.get_files(self.path_to_tx, chain)
        self.assertEqual(8, len(files))

    def test_get_files_in_add(self):
        chain = "ethereum"
        add_list = ['0x00000bec592ec7c143c73dc85804962075827ecc', '0x00000ce93aae3930abd880a4a9729c5618f3d691',
                    '0x0000ce08fa224696a819877070bf378e8b131acf', '0x000aa644afae99d06c9a0ed0e41b1e61beca958d',
                    '0x000ad8bc3dfbe42d9a87686f67c69001a2006da4', '0x000b94c47e4a8d7a70be12c50fc35722a7596972',
                    '0x000bec82c41837d974899b26b26f9cc8890af9ea', '0x000c93b5354c75f5319db0ec272c0dd900c07b83']
        files = self.dataLoader.get_files_in_address(chain, add_list)
        self.assertEqual(5, len(files))

    def test_get_address_name(self):
        file_name = "0x000bec82c41837d974899b26b26f9cc8890af9ea_tx.csv"
        address = self.dataLoader.get_address_name(file_name)
        self.assertEqual("0x000bec82c41837d974899b26b26f9cc8890af9ea", address)

    def test_load_df_tx(self):
        file_name = "0x000bec82c41837d974899b26b26f9cc8890af9ea_tx.csv"
        chain = "ethereum"
        df = self.dataLoader.load_df_tx(file_name, chain)
        self.assertEqual((743, 9), df.shape)

    def test_create_df_tx(self):
        chain = "ethereum"
        df = self.dataLoader.create_df_tx(chain)
        self.assertEqual(8, len(df.EOA.unique()))

    def test_create_df_tx_n(self):
        chain = "ethereum"
        n_files = 5
        df = self.dataLoader.create_df_tx(chain, n_files=n_files)
        self.assertEqual(n_files, len(df.EOA.unique()))

    def test_create_df_tx_add(self):
        chain = "ethereum"
        df = self.dataLoader.create_df_tx(chain, address_list=["0x000bec82c41837d974899b26b26f9cc8890af9ea"])
        self.assertEqual(1, len(df.EOA.unique()))


if __name__ == '__main__':
    unittest.main()
