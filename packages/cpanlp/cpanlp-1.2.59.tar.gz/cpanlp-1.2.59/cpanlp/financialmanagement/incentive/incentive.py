class Incentive:
    """
    Incentives are rewards or benefits given to individuals or groups to encourage certain behaviors or actions that align with the objectives of the organization.
    Features:
    - type: the type of incentive
    - amount: the amount of the incentive
    - recipients: the individuals or groups who will receive the incentive
    
    Methods:
    - __init__(type, amount, recipients): initializes a new Incentive object with the given type, amount, and recipients
    """
    def __init__(self, type, amount, recipients):
        self.type = type
        self.amount = amount
        self.recipients = recipients