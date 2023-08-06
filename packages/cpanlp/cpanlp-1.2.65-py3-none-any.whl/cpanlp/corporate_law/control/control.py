from cpanlp.corporate_law.control.power import *

class Control(VotingPower):
    """
    #### A class that represents a Control object which inherits from VotingPower.
    
    Features:
    - Inherits from VotingPower class.
    
    Args:
    - name (str): A string representing the name of the Control object.
    - voting_weight (float): A float representing the voting weight of the Control object.
    
    Methods:
    - __init__(self, name, voting_weight): Initializes a Control object with a name and voting weight.
    - get_control_power(self): Returns the control power of the Control object.
    """
    def __init__(self, name, voting_weight):
        super().__init__(name, voting_weight)
        if  self.voting_weight < 0.5 :
            raise ValueError("Control requires a voting weight bigger than 50%")
    def get_control_power(self):
        """
        Returns the control power of the Control object.
    
        Args:
        - None.
    
        Returns:
        - control_power (float): A float representing the control power of the Control object.
        """
        control_power = self.get_voting_power()
        return control_power