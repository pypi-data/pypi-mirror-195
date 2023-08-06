import datetime

class Certification:
    """
    #### A class representing a certification obtained by a person.

    Attributes:
    -----------
    name : str
        The name of the certification.
    date_obtained : datetime.date or None
        The date when the certification was obtained. If None, it means the certification has not been obtained yet.
    valid_until : datetime.date or None
        The date until which the certification is valid. If None, it means the certification never expires.

    Methods:
    --------
    is_valid() -> bool:
        Returns True if the certification is still valid, False otherwise.
    days_until_expiry() -> int or None:
        Returns the number of days until the certification expires. Returns None if the certification never expires.
    __str__() -> str:
        Returns a string representation of the certification.
    """
    def __init__(self, name, date_obtained=None,valid_until=None):
        self.name = name
        self.date_obtained = date_obtained
        self.valid_until = valid_until
    @property
    def is_valid(self) -> bool:
        """
        Returns True if the certification is still valid, False otherwise.
        """
        if self.date_obtained is None:
            return False
        elif self.valid_until is None:
            return True
        else:
            return self.valid_until >= datetime.date.today()

    def days_until_expiry(self) -> int or None:
        """
        Returns the number of days until the certification expires. Returns None if the certification never expires.
        """
        if self.valid_until is None:
            return 0
        else:
            delta = self.valid_until - datetime.date.today()
            return delta.days if delta.days >= 0 else 0

    def __str__(self) -> str:
        """
        Returns a string representation of the certification.
        """
        if self.date_obtained is None:
            return f"{self.name} (not obtained yet)"
        elif self.valid_until is None:
            return f"{self.name} (obtained on {self.date_obtained})"
        else:
            return f"{self.name} (obtained on {self.date_obtained}, valid until {self.valid_until})"