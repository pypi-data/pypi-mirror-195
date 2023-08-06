from cpanlp.event.acquisition.acquisition import *

class StrategicMerger(Acquisition):
    """
    #### A strategic merger is a type of acquisition that is focused on achieving specific strategic goals or objectives such as gaining market share, expanding product lines, or entering new markets.
    
    Attributes:
    - target_company: str
        The name of the target company being acquired.
    - acquiring_company: str
        The name of the acquiring company.
    - acquisition_ratio: float, optional
        The percentage of the target company being acquired.
    - strategic_goals: str, optional
        The strategic goals or objectives of the merger.
    - price: float, optional
        The total amount of money being paid for the acquisition.
    - leverage_ratio: float, optional
        The amount of debt being used to finance the acquisition.
    - date: str, optional
        The date on which the merger is taking place.
    """
    def __init__(self, target_company, acquiring_company,acquisition_ratio=None,strategic_goals=None,price=None,leverage_ratio=None,date=None):
        super().__init__(target_company, acquiring_company, acquisition_ratio, price,leverage_ratio,date)
        self.strategic_goals = strategic_goals