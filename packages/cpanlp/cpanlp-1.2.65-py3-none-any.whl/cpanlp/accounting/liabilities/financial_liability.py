from cpanlp.corporate_law.contract.financial_instruments.financial_instrument import *
from cpanlp.accounting.liabilities.liability import *
class FinancialLiability(Liability,FinancialInstrument):
    """
    #### A class representing a financial liability.
    #### A financial liability can be a contractual obligation, a payment involving an equity settlement, or a settlement of a derivative.

    Args:
    - account (str): The name of the liability account.
    - credit (float): The credit amount of the liability.
    - date (str): The date of the liability transaction.
    - due_date (str): The due date of the liability.
    - rate (float): The interest rate of the liability.
    - parties (dict): The parties involved in the liability transaction.
    - consideration (float): The consideration paid for the liability.
    - obligations (dict): The obligations associated with the liability.
    - value (float): The current value of the liability.
    """
    accounts = []
    def __init__(self, account, credit, date,due_date,rate,parties, consideration, obligations,value):
        Liability.__init__(self, account, credit, date,due_date,rate)
        FinancialInstrument.__init__(self,parties, consideration,obligations, value)
        FinancialLiability.accounts.append(self)


