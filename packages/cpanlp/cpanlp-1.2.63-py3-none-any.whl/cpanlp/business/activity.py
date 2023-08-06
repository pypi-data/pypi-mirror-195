class Activity:
    """
    #### Activity refers to a series of actions or processes typically associated with a goal or outcome, such as marketing activities, production activities, or financial activities. Activities typically involve multiple steps and participants and may require coordination across multiple departments or teams.
    
    Attributes:
    - name (str): The name of the activity.
    - value_added (float): The value added by the activity.

    Methods:
    - get_name() -> str: Returns the name of the activity.
    - get_value_added() -> float: Returns the value added by the activity.

    """
    def __init__(self, name, value_added):
        self.name = name
        self.value_added = value_added

    def get_name(self):
        return self.name

    def get_value_added(self):
        return self.value_added
