from cpanlp.accounting.assets.intangibleasset.intangibleasset import *

class IntellectualProperty(IntangibleAsset):
    """
    #### A class representing intellectual property as an intangible asset.
    #### Intellectual property is something that you create using your mind - for example, a story, an invention, an artistic work or a symbol.
    Args:
            account: The account associated with the intellectual property.
            debit: The debit balance of the intellectual property account.
            date: The date the intellectual property was acquired, in the format "YYYY-MM-DD".
            amortization_period: The number of years over which to amortize the cost of the intellectual property.
            owner: The owner of the intellectual property.
    """
    def __init__(self, account,debit, date,amortization_rate, owner,amortization_period):
        super().__init__(account,debit, date,amortization_rate,amortization_period)
        self.owner = owner
    def register_with_government(self):
        """
        #### Register the intellectual property with the government.
        """
        print(f"{self.owner} is registered with the government.")