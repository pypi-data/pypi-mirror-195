from cpanlp.event.certification.certification import *
class HighTechEnterpriseCertification(Certification):
    """
    #### A class representing a certification for a high-tech enterprise.

    Attributes:
    -----------
    name : str
        The name of the certification.
    RD_expenditure : float
        The amount of money spent on research and development.
    patent_count : int
        The number of patents held by the enterprise.
    revenue : float
        The total revenue of the enterprise.
    date_obtained : datetime.date or None
        The date when the certification was obtained. If None, it means the certification has not been obtained yet.
    valid_until : datetime.date or None
        The date until which the certification is valid. If None, it means the certification never expires.

    Methods:
    --------
    is_qualified() -> bool:
        Returns True if the enterprise meets the criteria for Hi-Tech Enterprise certification, False otherwise.
    get_status() -> str:
        Returns a string indicating the status of the enterprise's Hi-Tech Enterprise certification.
    """
    def __init__(self, name, RD_expenditure=None, patent_count=None, revenue=None,date_obtained=None,valid_until=None):
        super().__init__(name, date_obtained,valid_until)
        self.RD_expenditure = RD_expenditure if RD_expenditure is not None else 0
        self.patent_count = patent_count if patent_count is not None else 0
        self.revenue = revenue if revenue is not None else 0
    
    def is_qualified(self):
        """
        Returns True if the enterprise meets the criteria for Hi-Tech Enterprise certification, False otherwise.
        """
        if self.RD_expenditure / self.revenue >= 0.1 and self.patent_count >= 5:
            return True
        else:
            return False
    
    def get_status(self):
        """
        Returns a string indicating the status of the enterprise's Hi-Tech Enterprise certification.
        """
        if self.is_qualified():
            return f"{self.name} is certified as a Hi-Tech Enterprise."
        else:
            return f"{self.name} does not meet the criteria for Hi-Tech Enterprise certification."
