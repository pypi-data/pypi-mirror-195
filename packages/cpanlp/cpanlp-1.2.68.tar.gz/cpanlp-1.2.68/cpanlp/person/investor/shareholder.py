from cpanlp.person.investor.investor import *

class Shareholder(Investor):
    """
    #### A class representing a shareholder, who owns shares in a company.
    
    Attributes:
    - name (str): The name of the shareholder.
    - shares (int): The total number of shares owned by the shareholder.
    - expected_return (float): The expected return of the shareholder's portfolio.
    - risk_preference (float): The risk preference of the shareholder.
    - portfolio (dict): The portfolio of the shareholder, mapping stock symbols to the number of shares owned.
    - age (int): The age of the shareholder.
    - wealth (float): The wealth of the shareholder.
    - utility_function (function): The utility function of the shareholder.
    - restriction (str): The restriction on the shareholder's trading, if any.

    """
    
    def __init__(self,name,shares=None,expected_return=None, risk_preference=None, portfolio=None,age=None, wealth=None,utility_function=None ):
        super().__init__(name, age, wealth,utility_function,portfolio, expected_return, risk_preference)
        self.shares = shares
        self.restriction: None = None
    def vote_on_operating_policy(self):
        """
        Allows the shareholder to vote on the company's operating policy.
        """
        pass
    
    def vote_on_investment_plan(self):
        """
        Allows the shareholder to vote on the company's investment plan.
        """
        pass
    
    def vote_on_board_members(self):
        """
        Allows the shareholder to vote on the company's board members.
        """
        pass
    
    def vote_on_compensation(self):
        """
        Allows the shareholder to vote on the compensation for the company's board members.
        """
        pass
    
    def vote_on_financial_reports(self):
        """
        Allows the shareholder to vote on the company's financial reports.
        """
        pass
    
    def vote_on_profit_distribution(self):
        """
        Allows the shareholder to vote on the company's profit distribution.
        """
        pass
    
    def vote_on_capital_increase_or_decrease(self):
        """
        Allows the shareholder to vote on the company's capital increase or decrease.
        """
        pass
    
    def vote_on_bond_issuance(self):
        """
        Allows the shareholder to vote on the company's bond issuance.
        """
        pass
    
    def vote_on_merger_dissolution(self):
        """
        Allows the shareholder to vote on the company's merger, dissolution or change of company form.
        """
        pass
    
    def vote_on_amending_articles_of_incorporation(self):
        """
        Allows the shareholder to vote on amending the company's articles of incorporation.
        """
        pass