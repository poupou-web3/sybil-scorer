from polygonscan import PolygonScan
from src.main.utils.MineTx import MineTx


class MinePolygonTx(MineTx):
    def __init__(self, api_key, per_page_txn, api_counter):
        super().__init__(api_key, per_page_txn, api_counter)

    def get_txn_normal(self, address, page):
        with PolygonScan(self.api_key, False) as matic:
            return matic.get_normal_txs_by_address_paginated(
                address=address,
                startblock=0,
                endblock=99999999,
                sort="desc",
                page=page,
                offset=self.per_page_txn,
            )

    def get_txn_internal(self, address, page):
        with PolygonScan(self.api_key, False) as matic:
            return matic.get_internal_txs_by_address_paginated(
                address=address,
                startblock=0,
                endblock=99999999,
                sort="desc",
                page=page,
                offset=self.per_page_txn,
            )
