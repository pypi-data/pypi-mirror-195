class Department:
    """
    #### A class representing a department within a company.
    Attributes:
    - name (str): the name of the department.
    - goals (list[str]): the goals of the department.
    - incentives (list[str]): the incentives for the department.
    - legal_status (str): the legal status of the department, defaults to "Registered".
    - responsibility (list[str]): the responsibilities of the department.
    - powers (list[str]): the powers of the department.
    """
    def __init__(self, name, goals=None, incentives=None):
        self.name = name
        self.goals = goals
        self.incentives = incentives
        self.legal_status = "Registered"
        self.responsibility = []
        self.powers = []
