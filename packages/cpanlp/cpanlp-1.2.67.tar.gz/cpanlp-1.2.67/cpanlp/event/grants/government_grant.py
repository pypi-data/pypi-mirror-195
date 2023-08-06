from cpanlp.event.grants.grant import *

class GovernmentGrant(Grant):
    """
    A class representing a government grant.

    Attributes:
    -----------
    recipient : str or None
        The name of the recipient of the grant.
    donor : str or None
        The name of the organization or agency providing the grant.
    amount : float or None
        The amount of money provided by the grant.
    purpose : str or None
        The purpose or objective of the grant.
    deadline : datetime.date or None
        The deadline for the grant application or use of the grant funds.
    year : int or None
        The year in which the grant was awarded.

    Methods:
    --------
    increase_amount(amount: float) -> None:
        Increases the grant amount by the specified value.
    __str__() -> str:
        Returns a string representation of the government grant.
    """
    def __init__(self, recipient=None, donor=None, amount=None, purpose=None, deadline=None,year=None):
        super().__init__(recipient, donor, amount, purpose, deadline)
        self.year = year
    def __str__(self):
        return "Government Grants: Year - {}, Grant Name - {}, Grant Amount - {}".format(
            self.year, self.donor, self.amount
        )
        
    def increase_amount(self, amount):
        """
        Increases the grant amount by the specified value.

        Parameters:
        -----------
        amount : float
            The amount to increase the grant by.
        """
        self.amount += amount