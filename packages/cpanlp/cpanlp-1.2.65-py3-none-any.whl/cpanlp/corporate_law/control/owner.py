class Owner:
    """
    Features:
    - A class to represent an owner of assets or property.
    
    Args:
    - name (str): The name of the owner.
    - ownership_percentage (float): The percentage of ownership of the assets or property.
    - assets (list): The assets or property owned by the owner.
    
    Methods:
    - str(): Returns a string representation of the owner object.
    """
    def __init__(self, name, ownership_percentage, assets):
        self.name = name
        self.assets = assets
        self.ownership_percentage = ownership_percentage
    def __str__(self):
        return f"Name: {self.name}\nAssets: {self.assets}"

class BeneficialOwner(Owner):
    def __init__(self, name, assets,control_via,ownership_percentage=None):
        super().__init__(name, ownership_percentage, assets)
        self.control_via = control_via

    def __str__(self):
        return f"Name: {self.name}\nOwnership Percentage: {self.ownership_percentage}%\nAssets: {self.assets}"
