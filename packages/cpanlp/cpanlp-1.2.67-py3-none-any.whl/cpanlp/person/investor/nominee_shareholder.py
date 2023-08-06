from cpanlp.person.investor.shareholder import *

class NomineeShareholder(Shareholder):
    """
    #### A class representing a nominee shareholder, who is a designated representative that holds shares on behalf of the actual shareholder.
    
    Attributes:
    - actual_shareholder (str): The name of the actual shareholder.
    - name (str): The name of the nominee shareholder.
    - age (int): The age of the nominee shareholder.
    - wealth (float): The wealth of the nominee shareholder.
    - utility_function (function): The utility function of the nominee shareholder.
    - portfolio (dict): The portfolio of the nominee shareholder, mapping stock symbols to the number of shares owned.
    - expected_return (float): The expected return of the nominee shareholder's portfolio.
    - risk_preference (float): The risk preference of the nominee shareholder.
    - shares (int): The total number of shares owned by the nominee shareholder.
    """
    def __init__(self,actual_shareholder, name, age, wealth,utility_function,portfolio, expected_return, risk_preference,shares):
        super().__init__(name, age, wealth,utility_function,portfolio, expected_return, risk_preference,shares)
        self.actual_shareholder = actual_shareholder