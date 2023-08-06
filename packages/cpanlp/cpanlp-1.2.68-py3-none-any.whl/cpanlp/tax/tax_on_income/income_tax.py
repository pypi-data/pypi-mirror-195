from cpanlp.tax.tax import *

from cpanlp.tax.tax import Tax

class IncomeTax(Tax):
    """
    #### Represents an income tax, which is calculated based on a specified tax rate, a base amount, and tax deductions.

    Inherits from the Tax class.

    Attributes:
    - rate (float): The tax rate as a decimal.
    - base (float): The tax base amount.
    - deductions (float): The amount of tax deductions.

    Methods:
    - calculate(income: float) -> float: Calculates and returns the tax amount based on the income amount.
    """

    def __init__(self, rate, base, deductions):
        """
        Initializes an IncomeTax object with a specified tax rate, base amount, and tax deductions.

        Parameters:
        - rate (float): The tax rate as a decimal.
        - base (float): The tax base amount.
        - deductions (float): The amount of tax deductions.
        """
        super().__init__(rate, base, deductions)

    def calculate(self, income: float) -> float:
        """
        Calculates and returns the tax amount based on the income amount.

        Parameters:
        income (float): The income amount to be taxed.

        Returns:
        float: The amount of tax to be paid.
        """
        taxable_income = income - self.deductions
        return taxable_income * self.rate + self.base
