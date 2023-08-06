from cpanlp.person.consumer import *

class Creditor(Consumer):
    """
    #### The Creditor class represents a person or organization that has lent money to someone else.
    Attributes:
    - name (str): The name of the creditor.
    - age (int): The age of the creditor.
    - wealth (float): The wealth of the creditor.
    - utility_function (Utility): The utility function that represents the creditor's preferences.
    - amount (float): The amount of money lent.

    Methods:
    - lend_money: Lends money to someone else.
    """
    def __init__(self, name, amount=None, age=None, wealth=None,utility_function=None):
        super().__init__(name, age, wealth,utility_function)
        self.amount = amount
    def lend_money(self, debtor):
        """
        Lends money to someone else.
    
        Args:
        debtor (Debtor): The person or organization to lend money to.
    
        Returns:
        float: The amount of money lent.
        """
        # TODO: Implement the lend_money method
        pass