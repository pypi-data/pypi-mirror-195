from cpanlp.accounting.assets.asset import *
import random
import matplotlib.pyplot as plt

class IntangibleAsset(Asset):
    """
    #### A class representing an intangible asset.
    Args:
            account: The account associated with the intangible asset.
            debit: The debit balance of the intangible asset account.
            date: The date the intangible asset was acquired, in the format "YYYY-MM-DD".
            amortization_period: The number of years over which to amortize the cost of the intangible asset.
    """
    accounts = []
    def __init__(self,account,debit, date,amortization_rate,amortization_period):
        super().__init__(account, debit, date)
        if amortization_rate < 0 or amortization_rate > 1:
            raise ValueError("amortization_rate must be between 0 and 1")
        self.amortization_rate = amortization_rate
        self.amortization_history = []
        self.market_value = None
        self.competitive_advantage=None
        self.is_separable=True
        self.has_physical_substance=False
        self.non_monetary = True
        self.is_indefinite_lived = False
        self.amortization_period=amortization_period
        IntangibleAsset.accounts.append(self)
    def train(self):
        pass
    def predict(self, num_steps):
        pass
    def amortize(self):
        """
        Amortize the cost of the intangible asset over its useful life.
        """
        amortization_amount = self.debit * self.amortization_period
        self.amortization_history.append(amortization_amount)
        self.debit -= amortization_amount
    def simulate_volatility(self, volatility, num_steps):
        prices = [self.debit]
        for i in range(num_steps):
            prices.append(prices[-1] * (1 + volatility * random.uniform(-1, 1)))
        plt.plot(prices)
        plt.show()
    @classmethod
    def withdraw(cls, account, value):
        for equity in IntangibleAsset.accounts:
            if equity.account == account:
                equity.debit -= value
                break
    @classmethod
    def sum(cls):
        data = [[asset1.account, asset1.date, asset1.debit] for asset1 in IntangibleAsset.accounts]
        df = pd.DataFrame(data, columns=['账户类别', '日期', '借方金额'])
        return df