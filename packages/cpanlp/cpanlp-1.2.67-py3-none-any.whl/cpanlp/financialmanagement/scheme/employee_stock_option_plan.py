from datetime import datetime
class EmployeeStockOptionPlan:
    """
    An Employee Stock Option Plan (ESOP) is a type of compensation plan in which employees are granted options to purchase company stock at a pre-determined price. This class represents an individual employee's stock option plan and provides methods to determine if the plan is still valid and to calculate the plan's current value.

    Attributes:
    - option_grant (int): The number of stock options granted to the employee.
    - option_exercise_price (float): The price at which the employee can exercise their stock options.
    - option_expiration_date (datetime): The date on which the employee's stock options expire.
    """
    def __init__(self, option_grant, option_exercise_price, option_expiration_date):
        self.option_grant = option_grant
        self.option_exercise_price = option_exercise_price
        self.option_expiration_date = datetime.strptime(option_expiration_date, '%Y-%m-%d')
        
    def is_valid(self):
        """
        Returns True if the employee's stock options are still valid (i.e., the current date is before the option expiration date), False otherwise.
        """
        current_date = datetime.now().date()
        return current_date < self.option_expiration_date
    
    def value(self, current_stock_price):
        """
        Calculates the current value of the employee's stock options, based on the current stock price and the terms of the option plan.

        Args:
        - current_stock_price (float): The current market price of the company's stock.

        Returns:
        - The current value of the employee's stock options, as a float. If the options are no longer valid or are out of the money (i.e., the current stock price is less than or equal to the exercise price), returns 0.
        """
        if self.is_valid() and current_stock_price > self.option_exercise_price:
            return (current_stock_price - self.option_exercise_price) * self.option_grant
        else:
            return 0