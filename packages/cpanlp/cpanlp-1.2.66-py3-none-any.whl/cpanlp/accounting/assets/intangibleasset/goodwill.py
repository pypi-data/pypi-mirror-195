from cpanlp.accounting.assets.intangibleasset.intangibleasset import *

class Goodwill(IntangibleAsset):
    """
    #### A class representing goodwill as an intangible asset.
    Args:
            account: The account associated with the goodwill.
            debit: The debit balance of the goodwill account.
            date: The date the goodwill was acquired, in the format "YYYY-MM-DD".
            amortization_period: The number of years over which to amortize the cost of the goodwill.
    """
    def __init__(self,account,debit, date,amortization_rate,amortization_period):
        super().__init__(account,debit, date,amortization_rate,amortization_period)
    def __repr__(self) -> str:
        return f"Goodwill(account={self.account}, debit={self.debit}, date={self.date}) " 