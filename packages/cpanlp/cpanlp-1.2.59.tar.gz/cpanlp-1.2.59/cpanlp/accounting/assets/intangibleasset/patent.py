from cpanlp.accounting.assets.intangibleasset.intangibleasset import *

class Patent(IntangibleAsset):
    """
    #### A class representing a patent as an intangible asset.
    #### A patent is an exclusive right granted for an invention, which is a product or a process that provides, in general, a new way of doing something, or offers a new technical solution to a problem. 
    Args:
            name: The name of the patent.
            inventor: The inventor of the patent.
            patent_type: The type of the patent.
            account: The account associated with the patent.
            debit: The debit balance of the patent account.
            date: The date the patent was acquired, in the format "YYYY-MM-DD".
            amortization_period: The number of years over which to amortize the cost of the patent.
            patent_number: The number assigned to the patent by the patent office.
            application_date: The date the patent application was filed, in the format "YYYY-MM-DD".
            announcement_number: The number assigned to the patent announcement.
            certificate_number: The number assigned to the patent certificate.
    """
    def __init__(self, name=None,inventor=None, patent_type=None,account=None,debit=None, date=None,amortization_rate=None,patent_number=None, application_date=None, announcement_number=None, certificate_number=None,amortization_period=None):
        super().__init__(account,debit, date,amortization_rate,amortization_period)
        self.patent_number = patent_number
        self.application_date = application_date
        self.announcement_number = announcement_number
        self.certificate_number = certificate_number
        self.name=name
        self.inventor=inventor
        self.patent_type=patent_type
        
    def __str__(self):
        return "Patent: Name - {}, Patent number - {}, Application date - {}, Announcement number - {}, Certificate number - {}".format(
            self.name, self.patent_number, self.application_date, self.announcement_number, self.certificate_number
        )
        
    def is_valid(self):
        """
        #### Check if the patent is still valid.
        """
        print("The patent is still valid.")