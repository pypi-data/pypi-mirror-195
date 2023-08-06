class StockIssuanceValidator:
    """
    #### Stock issuance validator is a decorator that validates if a stock issuance is compliant with listing conditions and does not cause changes to the controlling shareholder or actual controller.
    """
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        # Add validation code here to check if the stock issuance
        # will cause the company's equity distribution to be
        # non-compliant with listing conditions, or cause changes
        # to the controlling shareholder or actual controller.
        if not self.check_equity_distribution(*args, **kwargs) or \
           not self.check_controlling_shareholder(*args, **kwargs):
            raise Exception("Stock issuance not compliant with conditions")

        # If everything is fine, call the decorated function.
        return self.func(*args, **kwargs)

    def check_equity_distribution(self, *args, **kwargs):
        """
        Check if the equity distribution is compliant with listing conditions
        """
        return False

    def check_controlling_shareholder(self, *args, **kwargs):
        """
        Check if the controlling shareholder or actual controller has changed
        """
        return True

