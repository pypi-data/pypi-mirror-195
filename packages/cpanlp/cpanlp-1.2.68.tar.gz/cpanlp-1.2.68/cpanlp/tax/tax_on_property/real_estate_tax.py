from cpanlp.tax.tax_on_property.property_tax import *

class RealEstateTax(PropertyTax):
    """
    #### A class for calculating real estate tax based on the property value, tax rate,deductions, and square footage.
    """
    def __init__(self, rate: float, base: float, deductions: float, value: float, square_footage: float):
        """
        Initializes a new instance of the RealEstateTax class.
        
        Args:
        - rate (float): The tax rate to be applied to the taxable value.
        - base (float): The basic amount of the property value that is not taxable.
        - deductions (float): The total amount of deductions that can be applied to the taxable value.
        - value (float): The value of the property.
        - square_footage (float): The total square footage of the property.
        """
        super().__init__(rate, base, deductions, value)
        self.square_footage = square_footage
    
    def calculate_tax(self) -> float:
        """
        #### Calculates the amount of real estate tax to be paid based on the value of the property,the tax rate, deductions, and square footage.
        
        Returns:
        float: The amount of real estate tax to be paid.
        """
        taxable_value = max(0, self.value - self.base - self.deductions)
        return round(taxable_value * self.rate * self.square_footage / 1000, 2)