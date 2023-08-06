from cpanlp.event.acquisition.merger import *

class StrategicMerger(Merger):
    """
    #### A class to represent a strategic merger between a target company and an acquiring company.

    Attributes:
    - target_company : str
        The name of the target company.
    - acquiring_company : str
        The name of the acquiring company.
    - merger_price : float, optional
        The price at which the merger took place, defaults to None.
    - strategic_goals : str, optional
        The strategic goals of the merger, defaults to None.
    - date : str, optional
        The date on which the merger took place, defaults to None
    """
    def __init__(self, target_company, acquiring_company, merger_price=None,strategic_goals=None,date=None):
        super().__init__(target_company, acquiring_company, merger_price,date)
        self.strategic_goals = strategic_goals