
class Commodity:
    """
    #### A commodity is a good or raw material that is bought and sold on the market. 
    
    Attributes:
    - commodity (str): The name of the commodity.
    - fair_value (float): The fair value of the commodity.
    - market_price (float): The current market price of the commodity.
    - supply (float): The total amount of the commodity available for sale.
    - demand (float): The total amount of the commodity being purchased.
    - gap (float): The difference between supply and demand.
    - supply_curve (dict): A dictionary containing the supply curve data.
    - demand_curve (dict): A dictionary containing the demand curve data.
    - level_of_standardization (str): The degree of standardization of the commodity.
    - ease_of_storage (str): The ease with which the commodity can be stored.
    - ease_of_transport (str): The ease with which the commodity can be transported.
    - level_of_substitutability (str): The degree to which the commodity can be substituted with other goods.
    - level_of_competition (str): The level of competition in the market.
    - fluctuation (float): The amount by which the market price of the commodity can fluctuate.
    
    Methods:
    - info: Prints out basic information about the commodity.
    - price_trend: Determines whether the price of the commodity is expected to increase, decrease, or remain stable.
    - get_supply_curve: Prints out the supply curve data.
    - get_demand_curve: Prints out the demand curve data.
"""
    def __init__(self, commodity, fair_value,market_price, supply, demand):
        self.commodity = commodity
        self.fair_value = fair_value
        self.market_price =market_price
        self.supply = supply
        self.demand = demand
        self.gap = self.demand - self.supply
        self.supply_curve = {}
        self.demand_curve = {}
        self.level_of_standardization = None
        self.ease_of_storage = None
        self.ease_of_transport = None
        self.level_of_substitutability = None
        self.level_of_competition = None
        self.fluctuation = None
    def info(self):
        print(f"Commodity: {self.commodity}")
        print(f"Fair value: {self.fair_value}")
        print(f"Supply: {self.supply}")
        print(f"Demand: {self.demand}")
    def price_trend(self):
        if self.supply > self.demand:
            print(f"The price of {self.commodity} is expected to decrease in the future")
        elif self.supply < self.demand:
            print(f"The price of {self.commodity} is expected to increase in the future")
        else:
            print(f"The price of {self.commodity} is expected to remain stable in the future")
    def get_supply_curve(self):
        print(f"The supply curve for {self.commodity} is as follows:")
        for price, quantity in self.supply_curve.items():
            print(f"Price: {price}, Quantity: {quantity}")   
    def get_demand_curve(self,demand_curve):
        print(f"The demand curve for {self.commodity} is as follows:")
        for price, quantity in demand_curve.items():
            print(f"Price: {price}, Quantity: {quantity}")