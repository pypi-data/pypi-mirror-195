class NonOperatingIncome:
    """
    #### Non-operating income is the portion of an organization's income that is derived from activities not related to its core business operations.
    #### Investment income, gains or losses from foreign exchange, as well as sales of assets, writedown of assets, interest income are all examples of non-operating income items.
    """
    def __init__(self, income_type="投资所得", amount=100, tax_rate=0.1, currency="RMB"):
        self.income_type = income_type
        self.amount = amount
        self.tax_rate = tax_rate
        self.currency = currency

    def calculate_tax(self):
        """
        #### Calculates the tax payable on the non-operating income based on the tax rate and amount.
        """
        return self.amount * self.tax_rate

    def to_usd(self, exchange_rate=6.5):
        """
        #### Converts the non-operating income amount from RMB to USD based on the exchange rate provided.
        """
        return self.amount / exchange_rate

    def __str__(self):
        """
        #### Returns a string representation of the NonOperatingIncome object.
        """
        return f"{self.amount} {self.currency} of {self.income_type} at {self.tax_rate*100}% tax rate"

