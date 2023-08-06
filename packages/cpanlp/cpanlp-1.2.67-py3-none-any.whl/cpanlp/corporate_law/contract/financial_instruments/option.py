from cpanlp.corporate_law.contract.financial_instruments.financial_instrument import *
import numpy as np
from scipy import stats
class Option(FinancialInstrument):
    """
    #### A class for pricing options.
    #### The term option refers to a financial instrument that is based on the value of underlying securities such as stocks.
    Attributes:
        stock_price (float): The current price of the underlying asset.
        strike_price (float): The price at which the option can be exercised.
        risk_free_rate (float): The risk-free interest rate.
        time_to_maturity (float): The time remaining until the option expires (in years).
        volatility (float): The volatility of the underlying asset's price.

    Methods:
        call_price() -> float: Calculates the price of a call option.
        put_price() -> float: Calculates the price of a put option.
    """
    def __init__(self, stock_price, strike_price, risk_free_rate, time_to_maturity, volatility,parties=None, consideration=None,obligations=None, value=None):
        super().__init__(parties, consideration,obligations, value)
        self.stock_price = stock_price
        self.strike_price = strike_price
        self.risk_free_rate = risk_free_rate
        self.time_to_maturity = time_to_maturity
        self.volatility = volatility

    def call_price(self):
        """
        #### Calculates the price of a call option.

        Returns:
            The price of a call option (float).
        """
        d1 = (np.log(self.stock_price / self.strike_price) + (self.risk_free_rate + 0.5 * self.volatility ** 2) * self.time_to_maturity) / (self.volatility * np.sqrt(self.time_to_maturity))
        d2 = d1 - self.volatility * np.sqrt(self.time_to_maturity)
        call_price = self.stock_price * stats.norm.cdf(d1) - self.strike_price * np.exp(-self.risk_free_rate * self.time_to_maturity) * stats.norm.cdf(d2)
        return call_price

    def put_price(self):
        """
        #### Calculates the price of a put option.

        Returns:
            The price of a put option (float).
        """
        d1 = (np.log(self.stock_price / self.strike_price) + (self.risk_free_rate + 0.5 * self.volatility ** 2) * self.time_to_maturity) / (self.volatility * np.sqrt(self.time_to_maturity))
        d2 = d1 - self.volatility * np.sqrt(self.time_to_maturity)
        put_price = self.strike_price * np.exp(-self.risk_free_rate * self.time_to_maturity) * stats.norm.cdf(-d2) - self.stock_price * stats.norm.cdf(-d1)
        return put_price

