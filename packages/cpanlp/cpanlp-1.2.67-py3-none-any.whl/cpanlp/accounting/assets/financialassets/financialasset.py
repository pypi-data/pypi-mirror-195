from cpanlp.corporate_law.contract.financial_instruments.financial_instrument import *
from cpanlp.accounting.assets.asset import *
import numpy as np
class FinancialAsset(Asset,FinancialInstrument):
    """
    #### This class represents a financial asset.

    Attributes:
    - account (str): the account associated with the financial asset.
    - debit (float): the value of the financial asset.
    - date (str): the date of financial asset recognition.
    - parties (list): a list of parties involved in the financial asset transaction.
    - consideration (float): the amount paid or received for the financial asset.
    - obligations (str): any obligations related to the financial asset.
    - value (float): the value of the financial asset.
    - accumulated_impairment (float): the total accumulated impairment of the financial asset. Default is 0.
    - market_values (list): a list of market values for the financial asset. Default is None.
    - investment_return (float): the investment return of the financial asset. Default is 0.
    - cash_flow (float): the cash flow of the financial asset. Default is 0.
    - cash_flows (np.array): an array of cash flows for the financial asset. Default is np.array(0).

    Methods:
    - impairment(): Calculates the impairment of the financial asset.
        plot_market_trend(): Plots the market trend of the financial asset.

    Example:
        stock1 = FinancialAsset("Tech Stocks", 100000, "2022-01-01", ["ABC Inc.", "XYZ Inc."], 50000, "None", 100000)
        stock1.market_values = [100, 120, 150, 130, 160]
        stock1.plot_market_trend()
        print(stock1.impairment())
        print(stock1)
    """

    accounts = []
    def __init__(self, account, debit,date,parties, consideration, obligations,value):
        Asset.__init__(self, account, debit,date)
        FinancialInstrument.__init__(self,parties, consideration,obligations, value)
        self.accumulated_impairment = 0
        self.market_values = None 
        self.investment_return = 0
        self.cash_flow = 0
        self.cash_flows=np.array(0)
        FinancialAsset.accounts.append(self)
        
    def impairment(self):
        """
        #### Calculates the impairment of the financial asset.

        Returns:
            float: The impairment of the financial asset.
        """
        # 假设减值准备的计算方式为财务资产的净值减去其市场价值
        net_value = self.debit  # 假设财务资产的净值为其当前价值
        impairment = net_value - self.market_value
        if impairment > 0:
            self.accumulated_impairment += impairment
    def __str__(self):
        return f"{self.account}: {self.debit} (Accumulated Impairment: {self.accumulated_impairment})"
    @property
    def roi(self):
        return (self.value - self.debit) / self.debit
    @property
    def cfar(self):
        cfar = (self.investment_return/self.cash_flow) * np.std(self.cash_flows)
        return cfar