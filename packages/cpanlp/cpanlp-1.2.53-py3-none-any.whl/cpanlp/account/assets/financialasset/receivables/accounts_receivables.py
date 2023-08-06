from cpanlp.account.assets.financialasset.financialasset import *
from datetime import datetime
class AccountsReceivable(FinancialAsset):
    """
    #### A class representing accounts receivable, which records money owed to a company by its customers.
    """
    accounts = []
    def __init__(self,account, debit,date,parties, consideration, obligations,value, due_date):
        super().__init__(account, debit,date,parties, consideration, obligations,value)
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        self.due_dates = {self.due_date: self.value}
        AccountsReceivable.accounts.append(self)
    def add_receivable(self, value, due_date):
        """
        #### Add a new receivable to the account.
        
        Args:
            value: The value of the receivable.
            due_date: The due date of the receivable, in the format "YYYY-MM-DD".
        """
        self.debit += value
        due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        if due_date in self.due_dates:
            self.due_dates[due_date] += value
        else:
            self.due_dates[due_date] = value
    def reduce_receivable(self, value, due_date):
        """
        #### Reduce the value of a receivable in the account.
        
        Args:
            value: The value of the receivable to be reduced.
            due_date: The due date of the receivable to be reduced, in the format "YYYY-MM-DD".
        """
        self.debit -= value
        due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        self.due_dates[due_date] -= value
    def check_due_date(self, date):
        """
        #### Check the total value of receivables due on or before a certain date.
        
        Args:
            date: The date to check, in the format "YYYY-MM-DD".
            
        Returns:
            The total value of receivables due on or before the given date.
        """
        total_due = 0.0
        date = datetime.strptime(date, "%Y-%m-%d").date()
        for d, v in self.due_dates.items():
            d = datetime.strptime(str(d), "%Y-%m-%d").date()
            if d <= date:
                total_due += v
        return total_due




