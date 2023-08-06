class GovernmentSubsidy:
    """
    #### A class representing a government subsidy for a product or service.
    #### Subsidies are financial assistance provided by the government to reduce the cost of certain products or services, making them more affordable for consumers, or to encourage production and sales in specific industries. 
    Attributes:
    -----------
    name : str or None
        The name of the subsidy.
    product_or_service : str or None
        The product or service that is being subsidised.
    original_price : float or None
        The original price of the product or service before the subsidy.
    subsidised_price : float or None
        The price of the product or service after the subsidy.
    year : int or None
        The year in which the subsidy was awarded.
    central_government_funds : float or None
        The amount of funds provided by the central government for the subsidy.
    special_funds : float or None
        The amount of special funds provided for the subsidy.

    Methods:
    --------
    total_amount() -> float:
        Returns the total amount of funds provided for the subsidy.
    __str__() -> str:
        Returns a string representation of the government subsidy.
    """
    def __init__(self,name=None, product_or_service=None, original_price=None, subsidised_price=None,year=None, central_government_funds=None, special_funds=None):
        self.name = name
        self.product_or_service = product_or_service
        self.original_price = original_price
        self.subsidised_price = subsidised_price
        self.year = year
        self.central_government_funds = central_government_funds if central_government_funds is not None else 0
        self.special_funds = special_funds if special_funds is not None else 0
        
    def __str__(self):
        return "Government Subsidy: Year - {}, Central government funds - {} million, Special funds - {} million".format(
            self.year, self.central_government_funds, self.special_funds
        )
        
    def total_amount(self):
        """
        Returns the total amount of funds provided for the subsidy.
        """
        return self.central_government_funds + self.special_funds
