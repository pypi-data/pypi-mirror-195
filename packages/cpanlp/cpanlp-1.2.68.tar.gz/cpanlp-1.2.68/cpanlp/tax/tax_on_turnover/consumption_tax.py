from cpanlp.tax.tax_on_turnover.turnover_tax import *

class ConsumptionTax(TurnoverTax):
    """
    A class for calculating consumption tax based on the turnover, tax rate,
    and deductions.
    """
    def __init__(self, rate: float, base: float, deductions: float):
        """
        Initializes a new instance of the ConsumptionTax class.
        
        Args:
        rate (float): The tax rate to be applied to the turnover.
        base (float): The basic amount of turnover that is not taxable.
        deductions (float): The total amount of deductions that can be applied to the taxable turnover.
        """
        super().__init__(rate, base, deductions)
    
    def calculate_tax(self, turnover: float) -> float:
        """
        Calculates the amount of consumption tax to be paid based on the turnover,
        the tax rate, and deductions.
        
        Args:
        turnover (float): The total amount of turnover.
        
        Returns:
        float: The amount of consumption tax to be paid.
        """
        taxable_turnover = max(0, turnover - self.base - self.deductions)
        return round(taxable_turnover * self.rate, 2)