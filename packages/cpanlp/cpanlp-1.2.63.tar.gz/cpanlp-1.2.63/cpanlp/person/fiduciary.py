from cpanlp.person.consumer import *

class Fiduciary(Consumer):
    """
    #### The Fiduciary class represents a person or entity that has a legal and ethical duty to act solely in the best interests of their beneficiaries.
    Attributes:
    - name (str): The name of the fiduciary.
    - beneficiary (Beneficiary): The beneficiary of the fiduciary.
    - age (int): The age of the fiduciary.
    - wealth (float): The wealth of the fiduciary.
    - utility_function (Utility): The utility function that represents the fiduciary's preferences.
    
    Methods:
    - invest: Invests funds on behalf of the beneficiary.
    - distribute_income: Distributes income to the beneficiary.
    - make_distributions: Makes distributions to the beneficiary.
    """
    def __init__(self, name, beneficiary=None, age=None,wealth=None, utility_function=None):
        super().__init__(name, age,wealth, utility_function)
        self.beneficiary = beneficiary
    def invest(self, amount, investment):
        """
        Invests funds on behalf of the beneficiary.
    
        Args:
        amount (float): The amount of funds to be invested.
        investment (Investment): The investment to be made.
        """
        print(f"${amount} has been invested in {investment} on behalf of {self.beneficiary}.")
        
    def distribute_income(self, amount):
        """
        Distributes income to the beneficiary.
    
        Args:
        amount (float): The amount of income to be distributed.
        """
        print(f"${amount} of income has been distributed to {self.beneficiary}.")
        
    def make_distributions(self, amount):
        """
        Makes distributions to the beneficiary.
    
        Args:
        amount (float): The amount of distributions to be made.
        """
        print(f"${amount} of distributions has been made to {self.beneficiary}.")