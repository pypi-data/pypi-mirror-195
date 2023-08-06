from cpanlp.tax.tax import *
from cpanlp.tax.tax import Tax

class BehaviorTax(Tax):
    """
    #### Represents a behavior tax, which is calculated based on a specified tax rate and a given behavior amount.

    Inherits from the Tax class.

    Attributes:
    - rate (float): The tax rate as a decimal.
    - base (float): The tax base amount.
    - deductions (float): The amount of tax deductions.
    - amount (float): The amount of the behavior to be taxed.

    Methods:
    - tax() -> float: Calculates and returns the tax amount based on the tax rate and behavior amount.
    """

    def __init__(self, rate: float, base: float, deductions: float, amount: float) -> None:
        """
        Initializes a BehaviorTax object with a specified tax rate, base amount, deductions, and behavior amount.

        Parameters:
        rate (float): The tax rate as a decimal.
        base (float): The tax base amount.
        deductions (float): The amount of tax deductions.
        amount (float): The amount of the behavior to be taxed.
        """
        super().__init__(rate, base, deductions)
        self.amount = amount

    @property
    def tax(self) -> float:
        """
        Calculates and returns the tax amount based on the tax rate and behavior amount.

        Returns:
        float: The amount of tax to be paid.
        """
        return self.amount * self.rate
