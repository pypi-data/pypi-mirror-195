from cpanlp.person.investor.shareholder import *

class ConsentingInvestor(Shareholder):
    """
    #### A consenting investor is a shareholder who has agreed to a particular action proposed by a company, such as a merger or acquisition.They have the right to vote on such actions and may either vote in favor or against them.
    Args:
    - name (str): The name of the investor.
    - action (str): The proposed action by the company.
    - age (int, optional): The age of the investor. Defaults to None.
    - wealth (float, optional): The wealth of the investor. Defaults to None.
    - utility_function (function, optional): The utility function of the investor. Defaults to None.
    - portfolio (list, optional): The investor's portfolio. Defaults to None.
    - expected_return (float, optional): The investor's expected return. Defaults to None.
    - risk_preference (float, optional): The investor's risk preference. Defaults to None.
    - shares (int, optional): The number of shares held by the investor. Defaults to None.
    
    Methods:
    - vote: The investor casts their vote in favor or against the proposed action.
    """
    def __init__(self, name=None, action=None,age=None, wealth=None,utility_function=None,portfolio=None, expected_return=None, risk_preference=None,shares=None):
        super().__init__(name, age, wealth,utility_function,portfolio, expected_return, risk_preference,shares)
        self.action = action
    def vote(self, decision):
        if decision == "in favor":
            print(f"{self.name} has voted in favor of the proposed action: {self.action}")
        elif decision == "against":
            print(f"{self.name} has voted against the proposed action: {self.action}")
        else:
            print("Invalid decision. Please vote either 'in favor' or 'against'.")