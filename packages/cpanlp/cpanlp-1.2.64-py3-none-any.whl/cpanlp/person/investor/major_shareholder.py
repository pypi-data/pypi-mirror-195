from cpanlp.person.investor.shareholder import *
class MajorShareholder(Shareholder):
    """
    #### A class representing a major shareholder, who holds more than 5% of the shares in a company.
    
    Attributes:
    - name (str): The name of the shareholder.
    - age (int): The age of the shareholder.
    - wealth (float): The wealth of the shareholder.
    - utility_function (function): The utility function of the shareholder.
    - portfolio (dict): The portfolio of the shareholder, mapping stock symbols to the number of shares owned.
    - expected_return (float): The expected return of the shareholder's portfolio.
    - risk_preference (float): The risk preference of the shareholder.
    - shares (int): The total number of shares owned by the shareholder.
    - voting_power (float): The voting power of the shareholder.
    """
    def __init__(self, name, age=None, wealth=None,utility_function=None,portfolio=None, expected_return=None, risk_preference=None,shares=None, voting_power=None):
        super().__init__(name, age, wealth,utility_function,portfolio, expected_return, risk_preference,shares)
        self.voting_power = voting_power