from cpanlp.markets.goods import *

class Sale(Goods):
    """
    #### A Sale is a type of Goods that has been sold to a customer. It includes information about the sale, such as the customer, quantity, unit price, and date.
    Attributes:
    - quarter (int): The quarter in which the sale occurred.
    - customer (str): The customer who purchased the goods.
    - quantity (float): The quantity of goods sold.
    - unit_price (float): The unit price at which the goods were sold.
    - date (str): The date on which the sale occurred.
    - supply_curve (dict): A dictionary representing the supply curve for the goods.
    - demand_curve (dict): A dictionary representing the demand curve for the goods.
    - accuracy (float): The accuracy of the data related to the sale.
    - completeness (float): The completeness of the data related to the sale.
    - validity (float): The validity of the data related to the sale.
    - growth_rate (float): The growth rate of the sale.
    - year (int): The year in which the sale occurred.
    - amount (float): The total amount of the sale.
    - amount_unit (str): The unit in which the total amount is measured.
    - segment (str): The segment of the market to which the goods were sold.
    - year_on_year (float): The year-on-year growth rate of the sale.
    - quarter_on_quarter (float): The quarter-on-quarter growth rate of the sale.
    - month_on_month (float): The month-on-month growth rate of the sale.
    """
    accounts = []
    def __init__(self, quarter=None, amount=None, amount_unit=None,growth_rate=None, segment=None,year=None,customer=None,goods=None, fair_value=None,market_price=None, supply=None, demand=None, quantity=None, unit_price=None,date=None,year_on_year=None,quarter_on_quarter=None,month_on_month=None):
        super().__init__(goods, fair_value,market_price, supply, demand)
        self.quarter=quarter
        self.customer=customer
        self.quantity = quantity if quantity is not None else 0.0
        self.unit_price = unit_price if unit_price is not None else 0.0
        self.date=date
        self.supply_curve = {1:3,1:4}
        self.demand_curve = {1:3,1:4}
        self.accuracy= None
        self.completeness = None
        self.validity = None
        self.growth_rate =growth_rate
        self.year = year
        self.amount = amount
        self.amount_unit =amount_unit
        self.segment= segment
        self.year_on_year = year_on_year
        self.quarter_on_quarter =quarter_on_quarter
        self.month_on_month = month_on_month
        Sale.accounts.append(self)


