from cpanlp.person.consumer import *

class Investor(Consumer):
    """
    #### An investor is an individual or entity that provides capital, typically in exchange for some form of ownership or return on investment. Investors can include individual investors, institutional investors, venture capital firms, and private equity firms, among others.

    Features:
    - portfolio: a list of investments made by the investor
    - expected_return: the expected return on investment for the investor
    - risk_preference: the investor's preference for risk

    Args:
    - name: the name of the investor
    - expected_return: the expected return on investment for the investor
    - risk_preference: the investor's preference for risk
    - portfolio: a list of investments made by the investor
    - age: the age of the investor
    - wealth: the wealth of the investor
    - utility_function: the utility function used by the investor to calculate their utility

    Methods:
    - set_portfolio: sets the portfolio of investments for the investor
    - set_expected_return: sets the expected return on investment for the investor
    - set_risk_preference: sets the investor's preference for risk
    - make_investment: makes an investment with expected return and risk preference
    """
    def __init__(self,name, expected_return=None, risk_preference=None,portfolio=None, age=None, wealth=None,utility_function=None):
        super().__init__(name, age,wealth, utility_function)
        self.portfolio = portfolio
        self.expected_return = expected_return
        self.risk_preference = risk_preference
    def set_portfolio(self, portfolio):
        self.portfolio = portfolio
    
    def set_expected_return(self, expected_return):
        self.expected_return = expected_return
    
    def set_risk_preference(self, risk_preference):
        self.risk_preference = risk_preference
    
    def make_investment(self):
        print(f"{self.name} makes an investment with expected return of {self.expected_return} and risk preference of {self.risk_preference}.")




