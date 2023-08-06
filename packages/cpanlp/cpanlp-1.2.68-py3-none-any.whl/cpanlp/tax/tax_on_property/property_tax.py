from cpanlp.tax.tax import *

class PropertyTax(Tax):
    """
    ### A class for calculating property tax based on the property value, tax rate, and deductions.
    
    Args:
    - rate (float): The tax rate to be applied to the taxable value.
    - base (float): The basic amount of the property value that is not taxable.
    - deductions (float): The total amount of deductions that can be applied to the taxable value.
    - value (float): The value of the property.
    """
    def __init__(self, rate: float, base: float, deductions: float, value: float):
        super().__init__(rate, base, deductions)
        self.value = value
    
    def calculate_tax(self) -> float:
        """
        Calculates the amount of property tax to be paid based on the value of the property,
        the tax rate, and deductions.
        
        Returns:
        float: The amount of property tax to be paid.
        """
        taxable_value = max(0, self.value - self.base - self.deductions)
        return round(taxable_value * self.rate, 2)
