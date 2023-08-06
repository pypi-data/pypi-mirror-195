from cpanlp.incentive.incentive import *

class EquityIncentive:
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
