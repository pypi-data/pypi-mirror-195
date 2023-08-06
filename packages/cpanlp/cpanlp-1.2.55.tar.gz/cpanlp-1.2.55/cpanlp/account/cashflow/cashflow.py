
from typing import List
class CashFlow:
    """
    #### A class representing a cash flow.
    #### Cash flow is the movement of money in and out of a company. Cash received signifies inflows, and cash spent signifies outflows. 
    Args:
            value: The amount of the cash flow.
            risk: The level of risk associated with the cash flow.
            timing: The timing of the cash flow.
    """
    accounts = []
    def __init__(self, value, risk, timing):
        self.value = value
        self.risk = risk
        self.timing = timing
        self.source = None
        self.is_positive= value > 0
        CashFlow.accounts.append(self)
    def __repr__(self) -> str:
            return f"CashFlow(value={self.value}, risk='{self.risk}', timing='{self.timing}')"
    def set_source(self, source: str) -> None:
        """
        #### Set the source of the cash flow.
        
        Args:
            source: The source of the cash flow.
        """
        self.source = source

    @property
    def predictability(self) -> str:
        """
        #### Calculate the predictability of the cash flow based on its historical data.
        
        Returns:
            The predictability of the cash flow, as a string.
        """
        # TODO: Implement predictability calculation
        return "High"

    @property
    def stability(self) -> str:
        """
        Calculate the stability of the cash flow based on its historical data.
        
        Returns:
            The stability of the cash flow, as a string.
        """
        # TODO: Implement stability calculation
        return "High"

    @property
    def growth_potential(self) -> str:
        """
        Calculate the growth potential of the cash flow based on its historical data.
        
        Returns:
            The growth potential of the cash flow, as a string.
        """
        # TODO: Implement growth potential calculation
        return "High"

    def calculate_npv(self, discount_rate: float, cash_flow_periods: List[float]) -> float:
        """
        Calculate the net present value (NPV) of the cash flow.
        
        Args:
            discount_rate: The discount rate to use in the calculation.
            cash_flow_periods: A list of cash flow periods in which the cash flow occurs.
        
        Returns:
            The net present value of the cash flow.
        """
        npv = 0
        for i, cf in enumerate(cash_flow_periods):
            npv += cf / (1 + discount_rate) ** i
        return npv

    def __str__(self) -> str:
        return f"Cash flow: value - {self.value}, risk level - {self.risk}, timing - {self.timing}"