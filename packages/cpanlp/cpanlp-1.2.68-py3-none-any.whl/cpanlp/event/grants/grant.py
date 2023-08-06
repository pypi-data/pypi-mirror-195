class Grant:
    """
    #### A class representing a grant.

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

    Methods:
    --------
    set_recipient(recipient: str) -> None:
        Sets the recipient of the grant.
    set_donor(donor: str) -> None:
        Sets the donor of the grant.
    set_amount(amount: float) -> None:
        Sets the amount of the grant.
    set_purpose(purpose: str) -> None:
        Sets the purpose of the grant.
    set_deadline(deadline: datetime.date) -> None:
        Sets the deadline for the grant application or use of the grant funds.
    """
    def __init__(self, recipient=None, donor=None, amount=None, purpose=None, deadline=None):
        self.recipient = recipient
        self.donor = donor
        self.amount = amount
        self.purpose = purpose
        self.deadline = deadline

    def set_recipient(self, recipient):
        """
        Sets the recipient of the grant.

        Parameters:
        -----------
        recipient : str
            The name of the recipient of the grant.
        """
        self.recipient = recipient

    def set_donor(self, donor):
        """
        Sets the donor of the grant.

        Parameters:
        -----------
        donor : str
            The name of the organization or agency providing the grant.
        """
        self.donor = donor

    def set_amount(self, amount):
        """
        Sets the amount of the grant.

        Parameters:
        -----------
        amount : float
            The amount of money provided by the grant.
        """
        self.amount = amount

    def set_purpose(self, purpose):
        """
        Sets the purpose of the grant.

        Parameters:
        -----------
        purpose : str
            The purpose or objective of the grant.
        """
        self.purpose = purpose

    def set_deadline(self, deadline):
        """
        Sets the deadline for the grant application or use of the grant funds.

        Parameters:
        -----------
        deadline : datetime.date
            The deadline for the grant application or use of the grant funds.
        """
        self.deadline = deadline
