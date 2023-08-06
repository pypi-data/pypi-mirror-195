from cpanlp.tax.tax_on_turnover.turnover_tax import *

class VAT(TurnoverTax):
    """
    #### A class for calculating value-added tax based on the turnover, tax rate,and deductions.
    Args:
    - rate (float): The tax rate to be applied to the turnover.
    - base (float): The basic amount of turnover that is not taxable.
    - deductions (float): The total amount of deductions that can be applied to the taxable turnover.
    """
    def __init__(self, rate: float, base: float, deductions: float):
        super().__init__(rate, base, deductions)