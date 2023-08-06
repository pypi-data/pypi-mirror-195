from datetime import datetime

class EmployeeStockOwnershipPlan:
    """
    #### An Employee Stock Ownership Plan (ESOP) is a type of defined contribution employee benefit plan in which the employer sets aside a portion of company stock and allocates it to individual employee accounts. This class represents an individual employee's ESOP and provides a method to calculate the number of vested shares based on the vesting period and cliff.

    Attributes:
    - employee_id (int): The unique identifier of the employee who owns the ESOP.
    - stock_symbol (str): The ticker symbol of the company's stock that is held in the ESOP.
    - shares_granted (int): The total number of shares of company stock granted to the employee in the ESOP.
    - grant_date (datetime): The date on which the shares were granted.
    - vesting_period (int): The number of days over which the shares vest.
    - vesting_cliff (int): The number of days after the grant date before the shares begin to vest.
    """
    def __init__(self, employee_id, stock_symbol, shares_granted, grant_date, vesting_period, vesting_cliff):
        self.employee_id = employee_id
        self.stock_symbol = stock_symbol
        self.shares_granted = shares_granted
        self.grant_date= datetime.strptime(grant_date, "%Y-%m-%d").date()
        self.vesting_period = vesting_period
        self.vesting_cliff = vesting_cliff
    def vest_shares(self, current_date):
        """
        Calculates the number of shares of company stock that have vested for the employee, based on the current date and the terms of the ESOP.

        Args:
        - current_date (str): The current date in 'YYYY-MM-DD' format.

        Returns:
        - The number of vested shares of company stock, as an integer.
        """
        time_elapsed = (datetime.strptime(current_date, "%Y-%m-%d").date() - self.grant_date).days
        if time_elapsed < self.vesting_cliff:
            return 0
        else:
            vested_shares = self.shares_granted * ((time_elapsed - self.vesting_cliff) / self.vesting_period)
            return min(vested_shares, self.shares_granted)