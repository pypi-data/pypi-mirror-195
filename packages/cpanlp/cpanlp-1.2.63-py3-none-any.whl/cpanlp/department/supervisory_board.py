from cpanlp.department.department import *
class SupervisoryBoard(Department):
    """
    #### A class representing the supervisory board department of a company.

    Attributes:
    - name (str): The name of the department.
    - goals (str or None): The department's goals.
    - incentives (str or None): The incentives for the department.
    - legal_status (str): The department's legal status, which is always "Registered".
    - responsibility (list): The department's responsibilities.
    - powers (list): The department's powers.
    - members (list): The members of the department.
    """

    def __init__(self, name, goals=None, incentives=None):
        """
        Initialize a new SupervisoryBoard object.

        Args:
        - name (str): The name of the department.
        - goals (str or None): The department's goals.
        - incentives (str or None): The incentives for the department.
        """
        super().__init__(name, goals, incentives)
        self.members = []