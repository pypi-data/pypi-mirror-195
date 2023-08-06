from cpanlp.markets.commodity import *
class Goods(Commodity):
    """
    #### A subclass of the Commodity class that represents goods or products that can be bought and sold on the market.
    
    Attributes:
    - goods (str): The name of the goods.
    - fair_value (float): The fair value of the goods.
    - market_price (float): The current market price of the goods.
    - supply (float): The total amount of the goods available for sale.
    - demand (float): The total amount of the goods being purchased.
    - gap (float): The difference between supply and demand.
    - supply_curve (dict): A dictionary containing the supply curve data.
    - demand_curve (dict): A dictionary containing the demand curve data.
    - level_of_standardization (str): The degree of standardization of the goods.
    - ease_of_storage (str): The ease with which the goods can be stored.
    - ease_of_transport (str): The ease with which the goods can be transported.
    - level_of_substitutability (str): The degree to which the goods can be substituted with other products.
    - level_of_competition (str): The level of competition in the market.
    - fluctuation (float): The amount by which the market price of the goods can fluctuate.
    
    Methods:
    - info: Prints out basic information about the goods.
    - price_trend: Determines whether the price of the goods is expected to increase, decrease, or remain stable.
    - get_supply_curve: Prints out the supply curve data.
    - get_demand_curve: Prints out the demand curve data.
    """

    def __init__(self, goods, fair_value,market_price, supply, demand):
        super().__init__(None, fair_value,market_price, supply, demand)
        self.goods=goods