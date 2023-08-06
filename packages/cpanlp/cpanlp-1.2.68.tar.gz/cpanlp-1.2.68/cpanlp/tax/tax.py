class Tax:
    """
    #### Represents a tax with a specified rate, base amount, and deductions.

    Attributes:
    - rate (float): The tax rate as a decimal.
    - base (float): The tax base amount.
    - deductions (float): The amount of tax deductions.
    - object (str): A description of the tax object.
    - payer (str): The person or entity responsible for paying the tax.
    - incentives (str): Any incentives or rebates associated with the tax.
    - deadline (str): The deadline for paying the tax.
    - location (str): The location where the tax must be paid.
    - history (list): A list of past payments made towards the tax.

    Methods:
    - add_payment(payment): Adds a payment to the tax payment history.
    - get_remaining_balance(): Calculates and returns the remaining balance of the tax after deductions and payments.
    """

    def __init__(self, rate, base, deductions):
        """
        Initializes a Tax object with a specified tax rate, base amount, and deductions.

        Parameters:
        - rate (float): The tax rate as a decimal.
        - base (float): The tax base amount.
        - deductions (float): The amount of tax deductions.
        """
        self.rate = rate
        self.base = base
        self.deductions = deductions
        self.object = None
        self.payer = None
        self.incentives = None
        self.deadline = None
        self.location = None
        self.history = []

    def add_payment(self, payment):
        """
        #### Adds a payment to the tax payment history.

        Parameters:
        - payment (float): The amount of the payment to be added.
        """
        self.history.append(payment)

    def get_remaining_balance(self):
        """
        #### Calculates and returns the remaining balance of the tax after deductions and payments.

        Returns:
        - float: The remaining balance of the tax.
        """
        total_payments = sum(self.history)
        remaining_balance = self.base - self.deductions - (total_payments * self.rate)
        return remaining_balance
