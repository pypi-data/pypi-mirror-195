from cpanlp.person.consumer import *
class Beneficiary(Consumer):
    """
    #### The Beneficiary class represents a beneficiary who receives the benefits of a trust or other arrangement.
    Attributes:
    - name (str): The name of the beneficiary.
    - age (int): The age of the beneficiary.
    - wealth (float): The wealth of the beneficiary.
    - utility_function (Utility): The utility function that represents the beneficiary's preferences.
    
    Methods:
    - receive_benefit: Receives the benefit of a trust or other arrangement.
    """
    def __init__(self, name, age=None,wealth=None, utility_function=None):
        super().__init__(name, age,wealth, utility_function)
    def receive_benefit(self, trust):
        """
        Receives the benefit of a trust or other arrangement.
    
        Args:
        trust (Trust): The trust or other arrangement from which the beneficiary will receive a benefit.
    
        Returns:
        float: The amount of the benefit received.
        """
        # TODO: Implement the receive_benefit method
        pass