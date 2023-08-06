from cpanlp.accounting.assets.intangibleasset.intangibleasset import *

class LandUseRight(IntangibleAsset):
    """
    #### A class representing land use rights as an intangible asset.
    Args:
            account: The account associated with the land use rights.
            debit: The debit balance of the land use rights account.
            date: The date the land use rights were acquired, in the format "YYYY-MM-DD".
            amortization_period: The number of years over which to amortize the cost of the land use rights.
            land_location: The location of the land.
    """
    def __init__(self, account,debit, date,amortization_rate, land_location,amortization_period):
        super().__init__(account,debit, date,amortization_rate,amortization_period)
        self.land_location = land_location
    def __repr__(self) -> str:
        return f"LandUseRight(account={self.account}, debit={self.debit}, date={self.date}, " \
               f"amortization_period={self.amortization_period}, land_location={self.land_location})"