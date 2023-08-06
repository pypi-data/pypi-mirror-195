from cpanlp.event.certification.certification import *

class QualifiedSupplierCertification(Certification):
    """
    #### A class representing a certification for a qualified supplier.

    Attributes:
    -----------
    supplier_name : str
        The name of the supplier.
    name : str
        The name of the certification.
    date_obtained : datetime.date or None
        The date when the certification was obtained. If None, it means the certification has not been obtained yet.
    valid_until : datetime.date or None
        The date until which the certification is valid. If None, it means the certification never expires.
    certification_obtained : bool
        Indicates whether the supplier has obtained the Qualified Supplier Certification or not.

    Methods:
    --------
    obtain_certification() -> None:
        Obtains the Qualified Supplier Certification for the supplier.
    is_certified() -> bool:
        Returns True if the supplier has obtained the Qualified Supplier Certification, False otherwise.
    """
    def __init__(self, supplier_name,name,date_obtained=None,valid_until=None):
        super().__init__(name, date_obtained,valid_until)
        self.supplier_name = supplier_name
        self.certification_obtained = False
        
    def obtain_certification(self):
        """
        Obtains the Qualified Supplier Certification for the supplier.
        """
        # logic to obtain certification, check criteria and requirements
        self.certification_obtained = True
        print(f"{self.supplier_name} has obtained the Qualified Supplier Certification.")
    @property    
    def is_certified(self):
        """
        Returns True if the supplier has obtained the Qualified Supplier Certification, False otherwise.
        """
        return self.certification_obtained