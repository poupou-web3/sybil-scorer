from etherscan import Etherscan
from sbscorer.utils.MineTx import MineTx


class MineEthTx(MineTx):
    def __init__(self, api_key, per_page_txn, api_counter):
        super().__init__(self, per_page_txn, api_counter)
        self.eth = Etherscan(api_key)

    def get_txn_normal(self, address, page):
        return self.eth.get_normal_txs_by_address_paginated(
            address=address,
            startblock=0,
            endblock=99999999,
            sort="desc",
            page=page,
            offset=self.per_page_txn,
        )

    def get_txn_internal(self, address, page):
        return self.eth.get_internal_txs_by_address_paginated(
            address=address,
            startblock=0,
            endblock=99999999,
            sort="desc",
            page=page,
            offset=self.per_page_txn,
        )
