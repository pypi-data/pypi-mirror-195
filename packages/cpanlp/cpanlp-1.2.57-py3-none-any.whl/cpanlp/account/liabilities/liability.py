import datetime
import pandas as pd
class Liability:
    """
    #### A class representing a financial liability.
    #### An amount of money in a company that is owed to someone and has to be paid in the future, such as tax, debt, interest, and mortgage payments.

    Args:
        account (str): The name of the liability account.
        credit (float): The credit amount of the liability.
        date (str): The date of the liability transaction.
        due_date (str): The due date of the liability.
        rate (float): The interest rate of the liability.
    """
    accounts = []
    def __init__(self, account, credit, date,due_date,rate):
        self.date=date
        self.account = account
        self.credit = credit
        self.due_date = due_date
        self.liabilities = []
        self.asset = None
        self.rate=rate
        today = datetime.date.today()
        due_date = datetime.datetime.strptime(self.due_date, "%Y-%m-%d").date()
        if today < due_date:
            self.remaining_days = (due_date - today).days
        else:
            raise ValueError("The liability has already expired and the remaining days cannot be calculated.")
        Liability.accounts.append(self)
    def make_payment(self, amount):
        """
        #### Make a payment on the liability.

        Args:
            amount (float): The amount to be paid.
        """
        self.credit -= amount
        print(f"{self.account} has made a payment of {amount}, and the remaining debt is {self.credit}.")
    def __str__(self):
        return f"Liability(account='{self.account}', amount={self.credit}, due_date='{self.due_date}')"
    def pay_liability(self,  account, amount):
        for liability in self.liabilities:
            if liability.account == account:
                    liability.amount -= amount
                    break
    def convert_to_equity(self, value):
        self.credit -= value
    def pay_off(self):
        if self.asset is not None:
            self.credit -= self.asset.debit
            self.asset = None
        else:
            raise ValueError("No asset to use for payment.")
    @classmethod
    def sum(cls):
        data = [[liability.account, liability.date, liability.credit] for liability in Liability.accounts]
        df = pd.DataFrame(data, columns=['账户类别', '日期', '贷方金额'])
        return df