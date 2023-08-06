from cpanlp.accounting.assets.asset import *
from collections import namedtuple
import pandas as pd

Costs = namedtuple('Costs', ('purchase_price', 'taxes', 'transportation_costs', 'installation_costs', 'professional_services_costs'))

#The most important attribute of a fixed asset is its ability to generate revenue or savings for the company. This can be through the asset's use in the production of goods or services, or through cost savings from the asset's use. Other important attributes of fixed assets include durability, reliability, and maintainability, as well as the asset's ability to retain its value over time. Additionally, factors such as the asset's useful life, as well as the company's ability to effectively utilize the asset, are also important to consider when evaluating a fixed asset.
class FixedAsset(Asset):
    """
    #### This class represents a fixed asset.

    Attributes:
    - account (str): the account associated with the asset.
    - debit (float): the value of the asset.
    - date (str): the date of asset recognition.
    - costs (list): a list of costs associated with the asset.
    - life_span (float): the useful life of the asset in years.
    - location (str): the location of the asset.

    Methods:
    - depreciate(rate): Calculates the depreciation of the asset.
    - total_cost(): Calculates the total cost of the asset.
    
    Example:
        asset1 = FixedAsset("Computer", 2000, "2022-01-01", [1500, 200], 5, "Room 101")
        asset1.depreciate(0.2)
        print(asset1.debit)
        print(asset1.total_cost())
    """
    accounts = []
    def __init__(self, account,debit,date,costs,life_span,location):
        super().__init__(account, debit, date)
        self.location=location
        self.costs= costs
        if life_span < 1:
            raise ValueError("Value must bigger than 1")
        self.life_span = life_span
        self.depreciation_history = []
        self.age = 0.0
        self.is_leased=False
        self.maintainability=True
        self.status = None
        self.depreciation_method=None
        self.cost_savings = None
        FixedAsset.accounts.append(self)
    def __str__(self):
        return f"{self.account} ({self.debit}), Location: {self.location}"
    def depreciate(self, rate):
        """
        #### Calculates the depreciation of the asset.

        Args:
            rate (float): The depreciation rate.

        Raises:
            ValueError: If the value is not between 0 and 1.
        """
        if rate < 0 or rate > 1:
            raise ValueError("Value must be between 0 and 1")
        if self.age < self.life_span:
            self.depreciation_history.append(rate * self.debit)
            a = rate * self.debit
            self.debit -= a
            self.age += 1
        else:
            print("Asset already reach its life span,no more depreciation.")

    def total_cost(self):
        """
        Calculates the total cost of the asset.

        Returns:
            float: The total cost of the asset.
        """
        return sum(self.costs)

    @classmethod
    def withdraw(cls, account, value):
        """
        Withdraws a value from the account.

        Args:
            account (str): The account associated with the asset.
            value (float): The value to withdraw.
        """
        for asset in FixedAsset.accounts:
            if asset.account == account:
                asset.debit -= value
                break

    @classmethod
    def sum(cls):
        """
        Calculates the sum of all fixed assets.

        Returns:
            pd.DataFrame: A dataframe representing the sum of all fixed assets.
        """
        data = [[asset.account, asset.date, asset.debit] for asset in FixedAsset.accounts]
        df = pd.DataFrame(data, columns=['Account', 'Date', 'Value'])
        return df
