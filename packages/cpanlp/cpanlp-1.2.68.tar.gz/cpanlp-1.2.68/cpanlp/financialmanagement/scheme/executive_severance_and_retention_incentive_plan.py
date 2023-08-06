class ExecutiveSeveranceAndRetentionIncentivePlan:
    """
    #### The Executive Severance and Retention Incentive Plan is a compensation plan designed to provide financial protection to eligible executives in the event of certain types of termination, and to incentivize them to remain with the company by offering retention bonuses.
    Args:
        - name (str): The name of the plan.
        - eligible_executives (list): A list of eligible executives who are covered by the plan.
        - severance_package (float): The amount of severance pay that eligible executives would receive in the event of certain types of termination.
        - retention_bonus (float): The amount of retention bonus that eligible executives would receive for remaining with the company for a specified period of time.
        - amended (bool): Whether the plan has been amended since it was first established. Default is False.
        - restated (bool): Whether the plan has been restated since it was first established. Default is False.
    """
    def __init__(self, name, eligible_executives, severance_package, retention_bonus, amended=False,restated=False):
        self.name = name
        self.eligible_executives = eligible_executives
        self.severance_package = severance_package
        self.retention_bonus = retention_bonus
        self.amended = amended
        self.restated=restated
