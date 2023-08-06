from cpanlp.account.assets.financialasset.receivables.accounts_receivables import *
class DividendReceivable(AccountsReceivable):
    accounts = []
    def __init__(self, account, debit,date,parties, consideration, obligations,value, due_date):
         super().__init__(account, debit,date,parties, consideration, obligations,value, due_date)
         DividendReceivable.accounts.append(self)