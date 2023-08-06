from typing import List
from cpanlp.corporate_law.contract.financial_instruments.financial_instrument import *
import pandas as pd

class Equity(FinancialInstrument):
    """
    #### A class representing equity ownership in a company.
    Args:
    - account: The name of the equity account.
    - credit: The credit amount of the equity.
    - date: The date of the equity transaction.
    - parties: The parties involved in the equity transaction.
    - consideration: The consideration paid for the equity.
    - obligations: The obligations associated with the equity.
    - value: The current value of the equity.
    """
    accounts = []
    def __init__(self, account, credit,date,parties, consideration, obligations,value):
        super().__init__(parties, consideration, obligations,value)
        self.credit=credit
        self.account = account
        self.date = date
        self.quality_of_underlying_assets=None
        Equity.accounts.append(self)
    def __str__(self):
        return f"{self.account}: {self.value}"
    @classmethod
    def withdraw(cls, account, value):
        for equity in Equity.accounts:
            if equity.account == account:
                equity.value -= value
                break
    @classmethod
    def sum(cls):
        data = [[asset.account, asset.date, asset.credit] for asset in Equity.accounts]
        df = pd.DataFrame(data, columns=['账户类别', '日期', '贷方金额'])
        return df
    @property
    def residual_ownership_interest(self) -> float:
        """
        Calculate the residual ownership interest of the equity.
        
        Returns:
            The residual ownership interest of the equity.
        """
        # TODO: Implement residual ownership interest calculation
        return 0.5

    @property
    def growth_potential(self) -> str:
        """
        Calculate the growth potential of the equity.
        
        Returns:
            The growth potential of the equity, as a string.
        """
        # TODO: Implement growth potential calculation
        return "High"

    @property
    def risk_return(self) -> str:
        """
        Calculate the risk-return profile of the equity.
        
        Returns:
            The risk-return profile of the equity, as a string.
        """
        # TODO: Implement risk-return profile calculation
        return "High risk, high return"

    @property
    def diversification(self) -> str:
        """
        Calculate the diversification benefits of the equity.
        
        Returns:
            The diversification benefits of the equity, as a string.
        """
        # TODO: Implement diversification benefits calculation
        return "Low"

    @property
    def liquidity(self) -> str:
        """
        Calculate the liquidity of the equity.
        
        Returns:
            The liquidity of the equity, as a string.
        """
        # TODO: Implement liquidity calculation
        return "Low"
