from cpanlp.accounting.assets.financialassets.financialasset import *
import pandas as pd
class Stock(FinancialAsset):
    """
    #### This class represents a stock.

    Attributes:
    - account (str): the account associated with the stock.
    - debit (float): the value of the stock.
    - date (str): the date of stock recognition.
    - parties (list): a list of parties involved in the stock transaction.
    - consideration (float): the amount paid or received for the stock.
    - obligations (str): any obligations related to the stock.
    - value (float): the value of the stock.
    - market_value (float): the market value of the stock.
    - symbol (str): the symbol of the stock.

    Methods:
    - sell(amount): Sells the specified amount of stock.
    - buy(amount): Buys the specified amount of stock.
    
    Example:
        stock1 = Stock("Tech Stocks", 100000, "2022-01-01", ["ABC Inc.", "XYZ Inc."], 50000, "None", 100000, 120000, "AAPL")
        stock1.sell(20000)
        stock1.buy(5000)
        print(stock1)
        print(Stock.sum())
    """
    accounts = []
    def __init__(self, account=None, debit=None,date=None,parties=None, consideration=None, obligations=None,value=None,market_value=None,symbol=None):
        super().__init__(account, debit,date,parties, consideration, obligations,value)
        self.market_value=market_value
        self.symbol = symbol
        Stock.accounts.append(self)
    def sell(self, amount):
        """
        Sells the specified amount of stock.

        Args:
            amount (float): The amount of stock to sell.
        """
        if amount > self.debit:
            raise ValueError("Cannot sell more than the current value of the asset.")
        self.debit -= amount
    def buy(self, amount):
        """
        Buys the specified amount of stock.

        Args:
            amount (float): The amount of stock to buy.
        """
        self.debit += amount
    def __str__(self):
        return f"Stock(account='{self.account}', value={self.debit}, symbol='{self.symbol}', market='{self.market_value}')"
    @classmethod
    def sum(cls):
        """
        Calculates the sum of all stocks.

        Returns:
            pd.DataFrame: A dataframe representing the sum of all stocks.
        """
        data = [[asset.account, asset.date, asset.debit] for asset in Stock.accounts]
        df = pd.DataFrame(data, columns=['Account', 'Date', 'Value'])
        return df