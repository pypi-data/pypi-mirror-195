from cpanlp.person.consumer import *

class Founder(Consumer):
    """
    #### The Founder class represents a person who is responsible for founding a company, and laying the groundwork for its vision,goals and strategies.
    
    Attributes:
    - name (str): The name of the founder.
    - age (int): The age of the founder.
    - wealth (float): The wealth of the founder.
    - utility_function (Utility): The utility function that represents the founder's preferences.
    - subscribed_shares (float): The number of shares subscribed to by the founder.
    - subscribed_shares_unit (str): The unit in which the subscribed shares are measured.
    - ownership_ratio (float): The ownership ratio of the founder in the company.
    - funding_method (str): The method used by the founder to raise funds.

    Methods:
    - set_subscribed_shares: Sets the number of shares subscribed to by the founder.
    - set_subscribed_shares_unit: Sets the unit in which the subscribed shares are measured.
    - set_ownership_ratio: Sets the ownership ratio of the founder in the company.
    - set_funding_method: Sets the method used by the founder to raise funds.
    """
    def __init__(self,name=None, age=None,wealth=None,utility_function=None, subscribed_shares=None, subscribed_shares_unit=None, ownership_ratio=None, funding_method=None):
        super().__init__(name, age,wealth,utility_function)
        self.subscribed_shares = subscribed_shares
        self.subscribed_shares_unit = subscribed_shares_unit
        self.ownership_ratio = ownership_ratio
        self.funding_method = funding_method
    def set_subscribed_shares(self, subscribed_shares):
        """
        Sets the number of shares subscribed to by the founder.
    
        Args:
        subscribed_shares (float): The number of shares subscribed to by the founder.
        """
        self.subscribed_shares = subscribed_shares
    
    def set_subscribed_shares_unit(self, subscribed_shares_unit):
        """
        Sets the unit in which the subscribed shares are measured.
    
        Args:
        subscribed_shares_unit (str): The unit in which the subscribed shares are measured.
        """
        self.subscribed_shares_unit = subscribed_shares_unit
    
    def set_ownership_ratio(self, ownership_ratio):
        """
        Sets the ownership ratio of the founder in the company.
    
        Args:
        ownership_ratio (float): The ownership ratio of the founder in the company.
        """
        self.ownership_ratio = ownership_ratio
    
    def set_funding_method(self, funding_method):
        """
        Sets the method used by the founder to raise funds.
    
        Args:
        funding_method (str): The method used by the founder to raise funds.
        """
        self.funding_method = funding_method
    
    
    
    