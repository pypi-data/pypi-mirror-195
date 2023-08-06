import numpy as np
import pandas as pd

#The most important attribute of an asset is its ability to generate cash flow or appreciate in value. This allows the asset to provide a return on investment or to be sold at a profit in the future. Additionally, the reliability and predictability of cash flow and appreciation are also important factors to consider when evaluating an asset.
class Asset:
    """
    #### This class represents an asset.

    Attributes:
        debit (float): the value of the asset.
        account (str): the account associated with the asset.
        date (str): the date of asset recognition.

    Methods:
        straight_line_depreciation(salvage_value, life): Calculates the straight-line depreciation of the asset.
        get_amortization_schedule(salvage_value, life, rate): Calculates the amortization schedule of the asset.
        is_asset_bubble(price): Determines if the asset is in a bubble.
        set_target(target_value): Sets a target value for the asset.
        check_target(): Checks if the asset has reached its target value.
    
    Example:
        asset1 = Asset(10000, "Cash", "2022-01-01")
        asset2 = Asset(5000, "Inventory", "2022-01-01")
        print(Asset.sum())
    Learn more about Asset in the [official documentation](https://en.wikipedia.org/wiki/Circle).
    """
    accounts = []
    def __init__(self, debit=None,account = None,date = None):
        self.account = account if account is not None else ""
        self.debit = debit if debit is not None else 0.0
        self.date = date if date is not None else ""
        self.assets=[]
        self.cashflows=[]
        self.is_measurable = True
        self.likely_economic_benefit = True
        self.potential_use=""
        self.market_value =debit if debit is not None else 0.0
        self.fair_value=None
        self.bubble=self.is_asset_bubble(self.market_value)
        self.target_value = None
        self.uniqueness= None
        Asset.accounts.append(self)
    def __repr__(self):
        return f"Asset({self.account}, {self.debit}, {self.date})"
    
    def straight_line_depreciation(self, salvage_value, life):
        """
    #### Calculates the straight-line depreciation of the asset.

    Args:
        salvage_value (float): The salvage value of the asset.
        life (int): The useful life of the asset in years.

    Returns:
        float: The annual depreciation of the asset.
    """
        annual_depreciation = (self.debit - salvage_value) / life
        return annual_depreciation
    def get_amortization_schedule(self, salvage_value, life, rate):
        """
        #### Calculates the amortization schedule of the asset.

        Args:
            salvage_value (float): The salvage value of the asset.
            life (int): The useful life of the asset in years.
            rate (float): The interest rate used for amortization.

        Returns:
            list: A list of tuples representing the amortization schedule.
        """
        schedule = []
        annual_depreciation = self.straight_line_depreciation(salvage_value, life)
        for year in range(1, life + 1):
            amortization = self.debit * rate
            depreciation = annual_depreciation
            self.debit -= (amortization + depreciation)
            schedule.append((year, amortization, depreciation))
        return schedule
    def is_asset_bubble(self, price) -> bool:
        return price > (3*self.debit)
    
    def set_target(self, target_value):
        self.target_value = np.array(target_value)
        
    def check_target(self):
        if self.target_value is not None:
            if np.all(self.debit > self.target_value):
                print(f"{self.account} has exceeded its target value")
            elif np.all(self.debit < self.target_value):
                print(f"{self.account} has not yet reached its target value")
            else:
                print(f"{self.account} has reached its target value")
        else:
            print(f"{self.account} has no target value set")
    @classmethod
    def withdraw(cls, account, value):
        for equity in Asset.accounts:
            if equity.account == account:
                equity.debit -= value
                break
    @classmethod
    def sum(cls):
        data = [[asset.account, asset.date, asset.debit] for asset in Asset.accounts]
        df = pd.DataFrame(data, columns=['账户类别', '日期', '借方金额'])
        return df