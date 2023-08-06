from cpanlp.financialmanagement.incentive.incentive import *

class EquityIncentive:
    """
    #### A type of incentive that provides employees with ownership in the company through equity (shares of stock).
    Features:
        - employee_name (str): Name of the employee receiving the equity incentive
        - position (str): Position of the employee
        - salary (float): Salary of the employee
        - equity (int): Number of equity shares awarded to the employee
    Args:
        employee_name (str): Name of the employee receiving the equity incentive
        position (str): Position of the employee
        salary (float): Salary of the employee
        equity (int): Number of equity shares awarded to the employee
    Methods:
        describe_equity_incentive: prints information about the equity incentive
    """
    def __init__(self, employee_name, position, salary, equity):
        self.employee_name = employee_name
        self.position = position
        self.salary = salary
        self.equity = equity
    
    def describe_equity_incentive(self):
        print("Employee Name: ", self.employee_name)
        print("Position: ", self.position)
        print("Salary: $", self.salary)
        print("Equity: ", self.equity, " shares")
