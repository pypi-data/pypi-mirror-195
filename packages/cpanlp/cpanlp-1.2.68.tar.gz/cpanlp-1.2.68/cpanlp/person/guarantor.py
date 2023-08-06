from cpanlp.person.consumer import *

class Guarantor(Consumer):
    """
    Guarantor class represents a consumer who provides a guarantee for another party's obligations.

    Features:
    - Guarantee type: the type of guarantee being provided
    - Guaranteed party: the party whose obligations are being guaranteed
    - Guaranteed obligations: the specific obligations being guaranteed

    Args:
    - name (str): name of the guarantor
    - guarantee_type (str): the type of guarantee being provided
    - guaranteed_party (str): the party whose obligations are being guaranteed
    - guaranteed_obligations (str): the specific obligations being guaranteed
    - age (int): age of the guarantor
    - wealth (float): wealth of the guarantor
    - utility_function (function): the utility function of the guarantor

    Methods:
    - set_guarantee_type(guarantee_type): set the guarantee type
    - set_guaranteed_party(guaranteed_party): set the guaranteed party
    - set_guaranteed_obligations(guaranteed_obligations): set the guaranteed obligations
    - issue_guarantee(): issue the guarantee
    """

    def __init__(self, name, guarantee_type=None, guaranteed_party=None, guaranteed_obligations=None,age=None,wealth=None,utility_function=None):
        super().__init__(name, age,wealth,utility_function)
        self.guarantee_type = guarantee_type
        self.guaranteed_party = guaranteed_party
        self.guaranteed_obligations = guaranteed_obligations
        
    def set_guarantee_type(self, guarantee_type):
        self.guarantee_type = guarantee_type
    
    def set_guaranteed_party(self, guaranteed_party):
        self.guaranteed_party = guaranteed_party
    
    def set_guaranteed_obligations(self, guaranteed_obligations):
        self.guaranteed_obligations = guaranteed_obligations
    
    def issue_guarantee(self):
        print(f"{self.name} issues a {self.guarantee_type} guarantee for {self.guaranteed_party} in relation to {self.guaranteed_obligations}.")
