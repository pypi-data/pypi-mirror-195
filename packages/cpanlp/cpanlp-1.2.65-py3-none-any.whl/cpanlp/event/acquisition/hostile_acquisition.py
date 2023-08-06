from cpanlp.event.acquisition.acquisition import *

class HostileAcquisition(Acquisition):
    """
    #### A class representing a hostile acquisition, which is an acquisition that is not approved or supported by the
    management of the target company.

    Attributes:
    - target_company (str): The name of the target company.
    - acquiring_company (str): The name of the acquiring company.
    - acquisition_ratio (float): The percentage of the target company that will be acquired by the acquiring company.
    - hostile_tactic (str): The tactic used by the acquiring company to gain control of the target company.
    - price (float): The price per share that will be paid for the acquisition.
    - leverage_ratio (float): The ratio of debt to equity that will be used to finance the acquisition.
    - date (str): The date on which the acquisition will take place.
    """
    def __init__(self, target_company, acquiring_company,acquisition_ratio=None,hostile_tactic=None,price=None,leverage_ratio=None,date=None):
        super().__init__(target_company, acquiring_company, acquisition_ratio, price,leverage_ratio,date)
        self.hostile_tactic = hostile_tactic