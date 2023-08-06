from cpanlp.accounting.assets.financialassets.financialasset import *
from datetime import datetime

class Bankdeposit(FinancialAsset):
    """
    #### This class represents a bank deposit as a financial asset.
    
    Attributes:
    - account: the account name or number associated with the deposit
    - debit: the current value of the deposit
    - date: the date the deposit was made
    - parties: the parties involved in the deposit
    - consideration: the consideration involved in the deposit
    - obligations: the obligations involved in the deposit
    - value: the total value of the deposit
    - interest_rate: the interest rate associated with the deposit
        
    Methods:
    - get_interest_earned: calculates the amount of interest earned on the deposit between the date of the deposit and the given end date, using the interest rate and the deposit amount. The result is returned as a float.

    """
    accounts = []
    def __init__(self, account, debit,date,parties, consideration, obligations,value, interest_rate):
        super().__init__(account, debit,date,parties, consideration, obligations,value)
        self.interest_rate = interest_rate
        Bankdeposit.accounts.append(self)
    def get_interest_earned(self, end_date: str) -> float:
        end_date1 = datetime.strptime(end_date, "%Y-%m-%d").date()
        start_date1 = datetime.strptime(self.date, "%Y-%m-%d").date()
        return (end_date1 - start_date1).days * self.interest_rate * self.debit
