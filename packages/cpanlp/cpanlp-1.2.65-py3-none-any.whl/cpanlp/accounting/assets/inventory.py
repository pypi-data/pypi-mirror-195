from cpanlp.accounting.assets.asset import *
import pandas as pd

class Inventory(Asset):
    """
    #### This class represents inventory.

    Attributes:
    - account (str): the account associated with the inventory.
    - debit (float): the value of the inventory.
    - date (str): the date of inventory recognition.
    - net_realizable_value (float): the net realizable value of the inventory.

    Methods:
    - value(): Calculates the value of the inventory.
    
    Example:
        inventory1 = Inventory("Raw Materials", 5000, "2022-01-01", 4500)
        print(inventory1.value())
        print(Inventory.sum())
    """
    accounts = []

    def __init__(self, account, debit, date, net_realizable_value):
        super().__init__(account, debit, date)
        self.net_realizable_value = net_realizable_value
        self.impairment_loss = max(0, self.debit - self.net_realizable_value)
        self.quality = None
        self.turnover_rate = None
        self.level_of_obsolescence = None
        self.is_confirmed = (
            self.likely_economic_benefit and self.is_measurable)
        self.items = []  # list to store inventory items
        self.classifier = None
        Inventory.accounts.append(self)

    def value(self):
        """
        #### Calculates the value of the inventory.

        Returns:
            float: The value of the inventory.
        """
        return min(self.debit, self.net_realizable_value)

    @classmethod
    def withdraw(cls, account, value):
        """
        #### Withdraws a value from the account.

        Args:
            account (str): The account associated with the inventory.
            value (float): The value to withdraw.
        """
        for equity in Inventory.accounts:
            if equity.account == account:
                equity.debit -= value
                break

    @classmethod
    def sum(cls):
        """
        #### Calculates the sum of all inventories.

        Returns:
            pd.DataFrame: A dataframe representing the sum of all inventories.
        """
        data = [[asset.account, asset.date, asset.debit]
                for asset in Inventory.accounts]
        df = pd.DataFrame(data, columns=['账户类别', '日期', '借方金额'])
        return df
