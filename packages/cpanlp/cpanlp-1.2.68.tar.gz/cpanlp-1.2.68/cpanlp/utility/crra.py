import numpy as np

class CRRA:
    """
    #### A class representing a Constant Relative Risk Aversion utility function.
    Args:
    - gamma (float): The coefficient of relative risk aversion.
    """
    def __init__(self, gamma: float):
        self.gamma = gamma
    
    def utility(self, c: float) -> float:
        """
        #### Calculates the utility of consuming a given amount of a good or service.
        
        Args:
        c (float): The amount of the good or service consumed.
        
        Returns:
        float: The utility of consuming the good or service.
        """
        if self.gamma == 1.:
            return np.log(c)
        else:
            return (c ** (1 - self.gamma)) / (1 - self.gamma)
