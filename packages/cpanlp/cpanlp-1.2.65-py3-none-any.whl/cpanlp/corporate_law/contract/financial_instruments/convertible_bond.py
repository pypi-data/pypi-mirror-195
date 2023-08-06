from cpanlp.corporate_law.contract.financial_instruments.bond import *
class ConvertibleBond(Bond):
    """
    #### A class representing a convertible bond financial instrument.
    
    Attributes:
    - issuer (str): The issuer of the convertible bond.
    - coupon (float): The coupon rate of the convertible bond.
    - conversion_price (float): The conversion price of the convertible bond.
    - maturity_date (str): The maturity date of the convertible bond.
    - parties (list[str]): A list of parties involved in the convertible bond agreement.
    - value (float): The monetary value of the convertible bond.
    - rate (float): The interest rate of the convertible bond.
    - currency (str): The currency of the convertible bond.
    - domestic (bool): Whether the convertible bond is domestic or international.
    - outstanding_balance (float): The outstanding balance of the convertible bond.
    - date (str): The date of the convertible bond issuance.
    
    Methods:
    - set_issuer(issuer: str): Set the issuer of the convertible bond.
    - set_coupon(coupon: float): Set the coupon rate of the convertible bond.
    - set_conversion_price(conversion_price: float): Set the conversion price of the convertible bond.
    - set_maturity_date(maturity_date: str): Set the maturity date of the convertible bond.

    """
    def __init__(self, issuer=None, coupon=None, conversion_price=None, maturity_date=None,parties=None, consideration=None,obligations=None, value=None,rate=None,currency=None,domestic=None,date=None,outstanding_balance=None):
        super().__init__(parties,value, rate, currency,domestic,date,consideration, obligations,outstanding_balance)
        self.issuer = issuer
        self.coupon = coupon
        self.conversion_price = conversion_price
        self.maturity_date = maturity_date

    def set_issuer(self, issuer):
        """
        #### Set the issuer of the convertible bond.

        Args:
        issuer (str): The issuer to be set.
        """
        self.issuer = issuer

    def set_coupon(self, coupon):
        """
        #### Set the coupon rate of the convertible bond.

        Args:
        coupon (float): The coupon rate to be set.
        """
        self.coupon = coupon

    def set_conversion_price(self, conversion_price):
        """
        Set the conversion price of the convertible bond.

        Args:
        conversion_price (float): The conversion price to be set.
        """
        self.conversion_price = conversion_price

    def set_maturity_date(self, maturity_date):
        """
        Set the maturity date of the convertible bond.

        Args:
        maturity_date (str): The maturity date to be set.
        """
        self.maturity_date = maturity_date