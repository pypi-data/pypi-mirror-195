from cpanlp.utility.crra import *

from cpanlp.utility.crra import CRRA

class CRRAInvestor(CRRA):
    """
    #### A class representing an investor with a CRRA utility function and a risk aversion parameter.
    """
    def __init__(self, gamma, rho):
        """
        Initializes a new instance of the CRRAInvestor class.
        
        Args:
        - gamma (float): The coefficient of relative risk aversion.
        - rho (float): The risk aversion parameter.
        """
        super().__init__(gamma)
        self.rho = rho
    
    def utility(self, c, w) -> float:
        """
        #### Calculates the utility of consuming a given amount of a good or service and investing a given amount of wealth in a risky asset.
        
        Args:
        c (float): The amount of the good or service consumed.
        w (float): The amount of wealth invested in a risky asset.
        
        Returns:
        float: The utility of consuming the good or service and investing in the risky asset.
        """
        if self.gamma == 1:
            return np.log(c) + self.rho * np.log(w)
        else:
            return (c ** (1 - self.gamma)) / (1 - self.gamma) + self.rho * (w ** (1 - self.gamma)) / (1 - self.gamma)
