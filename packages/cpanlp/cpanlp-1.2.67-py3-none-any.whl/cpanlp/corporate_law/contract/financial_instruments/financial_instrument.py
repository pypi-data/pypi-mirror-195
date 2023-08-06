from cpanlp.corporate_law.contract.contract import *
class FinancialInstrument(Contract):
    """
    #### A class representing a financial instrument.
    Attributes:
    - parties (list[str]): A list of parties involved in the financial instrument agreement.
    - consideration (str): The consideration for the financial instrument.
    - obligations (str): The obligations for the financial instrument.
    - value (float): The monetary value of the financial instrument.
    
    Methods:
    - get_value(): Get the monetary value of the financial instrument.
    """
    accounts = []
    def __init__(self,parties=None, consideration=None,obligations=None, value=None):
        super().__init__(parties, consideration,obligations)
        self.value = value if value is not None else 0.0
        FinancialInstrument.accounts.append(self)
    def get_value(self):
        """
        #### Get the monetary value of the financial instrument.
    
        Returns:
        The monetary value of the financial instrument.
        """
        return self.value
    