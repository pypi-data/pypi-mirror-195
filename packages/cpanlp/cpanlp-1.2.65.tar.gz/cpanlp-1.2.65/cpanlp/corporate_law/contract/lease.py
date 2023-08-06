from cpanlp.corporate_law.contract.contract import *

class Lease(Contract):
    """
    Features:
    - Leases are contracts used for renting property or equipment.
    - Leases typically involve a lessor (owner of the property) and a lessee (renter).
    
    Args:
    - parties: a list of parties involved in the lease agreement.
    - consideration: the amount of rent to be paid by the lessee to the lessor.
    - obligations: the responsibilities of each party under the lease agreement.
    - property_address: the address of the property being leased.
    
    Methods:
    - calculate_rent(): calculates the amount of rent to be paid for a given period.
    - track_payments(): tracks lease payments and expenses.
    - terminate_lease(): allows for the early termination of the lease agreement.
    """
    accounts = []
    def __init__(self, parties=None, consideration=None,obligations=None, property_address=None):
        super().__init__(parties, consideration,obligations)
        self.property_address = property_address
        self.rent = consideration
        self.economic_benefits = True
        self.use_direction = True
        Lease.accounts.append(self)
    def calculate_rent(self, period):
        """Calculates the rent to be paid for the given period."""
        # Code to calculate the rent amount goes here.
        pass
    
    def track_payments(self):
        """Tracks lease payments and expenses."""
        # Code to track lease payments and expenses goes here.
        pass
    
    def terminate_lease(self):
        """Allows for the early termination of the lease agreement."""
        # Code to terminate the lease agreement goes here.
        pass
    
    def definition(self):
        return "Paragraph 9 of IFRS 16 states that ‘a contract is, or contains, a lease if the contract conveys the right to control the use of an identified asset for a period of time in exchange for consideration'"