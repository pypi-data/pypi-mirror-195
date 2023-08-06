from cpanlp.tax.tax_on_behavior.behavior_tax import *

class TransactionTax(BehaviorTax):
    """
    #### Represents a transaction tax, which is calculated based on a specified tax rate and a given transaction amount.

    #### Inherits from the BehaviorTax class.

    Attributes:
    - rate (float): The tax rate as a decimal.
    - base (float): The tax base amount.
    - deductions (float): The amount of tax deductions.
    - amount (float): The amount of the behavior to be taxed.
    - transaction (float): The amount of the transaction to be taxed.

    Methods:
    - tax(): Calculates and returns the tax amount based on the tax rate and transaction amount.
    """

    def __init__(self, rate, base, deductions, amount, transaction):
        """
        Initializes a TransactionTax object with a specified tax rate, base amount, deductions, behavior amount,
        and transaction amount.

        Parameters:
        rate (float): The tax rate as a decimal.
        base (float): The tax base amount.
        deductions (float): The amount of tax deductions.
        amount (float): The amount of the behavior to be taxed.
        transaction (float): The amount of the transaction to be taxed.
        """
        super().__init__(rate, base, deductions, amount)
        self.transaction = transaction

    @property
    def tax(self):
        """
        Calculates and returns the tax amount based on the tax rate and transaction amount.

        Returns:
        float: The amount of tax to be paid.
        """
        return self.transaction * self.rate
