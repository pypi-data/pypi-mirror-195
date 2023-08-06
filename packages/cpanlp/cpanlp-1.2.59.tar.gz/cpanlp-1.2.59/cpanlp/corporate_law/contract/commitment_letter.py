from cpanlp.corporate_law.contract.contract import *

class CommitmentLetter(Contract):
    """
    #### Commitment Letter is a type of contract used in the securities market. It is an agreement signed by a buyer and seller,committing to complete a stock transaction at some point in the future. Commitment letters are a common way of trading stocks on the securities market.

    Features:
    - Detailed information: Commitment letters typically include detailed information about the transaction, such as the transaction price, quantity, and date.
    - Obligations: Both the buyer and seller have an obligation to adhere to the agreement and complete the transaction on the agreed-upon date. Failure to do so can result in financial losses or legal liability.
    - Evaluation: Investors should carefully evaluate the market conditions before signing a commitment letter to ensure that the transaction is reasonable. Additionally, investors should work with legal advisors to ensure the legality and enforceability of the commitment letter.

    Args:
    - commitment (str): The commitment letter identifier.
    - buyer (str): The name of the buyer.
    - seller (str): The name of the seller.
    - stock_symbol (str): The stock symbol of the stock being traded.
    - price (float): The transaction price.
    - quantity (int): The quantity of shares being traded.
    - date (str): The agreed-upon date for the transaction.

    Methods:
    - set_buyer(buyer): Set the name of the buyer.
    - set_seller(seller): Set the name of the seller.
    - set_stock_symbol(stock_symbol): Set the stock symbol of the stock being traded.
    - set_price(price): Set the transaction price.
    - set_quantity(quantity): Set the quantity of shares being traded.
    - set_date(date): Set the agreed-upon date for the transaction.
    """
    def __init__(self,commitment=None, buyer=None, seller=None, stock_symbol=None, price=None, quantity=None, date=None,parties=None, consideration=None,obligations=None):
        super().__init__(parties, consideration,obligations)
        self.commitment = commitment
        self.buyer = buyer
        self.seller = seller
        self.stock_symbol = stock_symbol
        self.price = price
        self.quantity = quantity
        self.date = date

    def set_buyer(self, buyer):
        self.buyer = buyer

    def set_seller(self, seller):
        self.seller = seller

    def set_stock_symbol(self, stock_symbol):
        self.stock_symbol = stock_symbol

    def set_price(self, price):
        self.price = price

    def set_quantity(self, quantity):
        self.quantity = quantity

    def set_date(self, date):
        self.date = date


