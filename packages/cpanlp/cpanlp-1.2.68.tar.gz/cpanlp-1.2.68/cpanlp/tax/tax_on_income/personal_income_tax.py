from cpanlp.tax.tax_on_income.income_tax import *

from cpanlp.tax.tax_on_income.income_tax import IncomeTax

class PersonalIncomeTax(IncomeTax):
    """
    #### Represents a personal income tax, which is calculated based on a specified tax rate, a base amount,
    tax deductions, and tax exemptions.

    Inherits from the IncomeTax class.

    Attributes:
    - rate (float): The tax rate as a decimal.
    - base (float): The tax base amount.
    - deductions (float): The amount of tax deductions.
    - exemptions (float): The amount of tax exemptions.

    Methods:
    - calculate(income: float) -> float: Calculates and returns the tax amount based on the income amount,
    tax deductions, and tax exemptions.
    """

    def __init__(self, rate, base, deductions, exemptions):
        """
        Initializes a PersonalIncomeTax object with a specified tax rate, base amount, tax deductions, and tax exemptions.

        Parameters:
        rate (float): The tax rate as a decimal.
        base (float): The tax base amount.
        deductions (float): The amount of tax deductions.
        exemptions (float): The amount of tax exemptions.
        """
        super().__init__(rate, base, deductions)
        self.exemptions = exemptions

    def calculate(self, income: float) -> float:
        """
        Calculates and returns the tax amount based on the income amount, tax deductions, and tax exemptions.

        Parameters:
        income (float): The income amount to be taxed.

        Returns:
        float: The amount of tax to be paid.
        """
        taxable_income = income - self.deductions - self.exemptions
        return taxable_income * self.rate + self.base
