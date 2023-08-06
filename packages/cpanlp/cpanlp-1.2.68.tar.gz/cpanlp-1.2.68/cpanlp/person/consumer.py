
from cpanlp.utility.crra import *
from scipy.optimize import minimize
import math
import numpy as np
class Consumer:
    """
    The Consumer class represents a consumer in an economic model.
    Attributes:
    - name (str): The name of the consumer.
    - age (int): The age of the consumer.
    - wealth (float): The amount of wealth that the consumer has.
    - commodity_prices (list): A list of the prices of the commodities that the consumer is interested in purchasing.
    - utility_function (Utility): The utility function that represents the consumer's preferences.
    
    Methods:
    - calculate_utility: Calculates the total utility for a consumer given a set of goods, their prices, and the consumer's income.
    - indifference_curve: The indifference curve function.
    - budget_constraint: The budget constraint function.
    - optimize_utility: Finds the optimal bundle of goods that maximizes the consumer's utility.
    """
    def __init__(self, name, age=None,wealth=None, utility_function=None):
        self.name = name
        self.age = age
        self.wealth= wealth
        self.commodity_prices=[]
        self.utility_function = utility_function
    def calculate_utility(self, goods, prices):
        """
        Calculates the total utility for a consumer given a set of goods, their prices, and the consumer's income.

        Args:
        - goods (list): A list of the quantities of the goods being purchased.
        - prices (list): A list of the prices of the goods being purchased.

        Returns:
        - float: The total utility of the consumer.
        """
        total_utility = 0
        for i in range(len(goods)):
            total_utility += math.log(np.log(goods[i]) - prices[i] / self.wealth)
        return total_utility
    def indifference_curve(self, x):
        """
        The indifference curve function.

        Args:
        x (list): A list of the quantities of the goods being purchased.

        Returns:
        float: The value of the indifference curve function.
        """
        # Indifference curve function
        # U(x1,x2) = sqrt(x1) + sqrt(x2)
        # Budget constraint: p1*x1 + p2*x2 <= income
        U=self.utility_function
        return U(x[0]) + U(x[1])
    def budget_constraint(self, x):
        p1, p2 = self.commodity_prices
        return p1 * x[0] + p2 * x[1] - self.wealth
    def optimize_utility(self,prices):
        self.commodity_prices=prices
        x0 = [2, 2]
        bounds=[[0,None],[0,None]]
        constraints = {'type': 'ineq', 'fun': self.budget_constraint}
        res = minimize(self.indifference_curve, x0, bounds=bounds,constraints=constraints)
        return res.x