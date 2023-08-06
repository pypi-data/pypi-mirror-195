from cpanlp.person.consumer import *

class Craftsman(Consumer):
    """
    The Craftsman class represents a skilled worker who produces goods by hand.
    Attributes:
    - name (str): The name of the craftsman.
    - age (int): The age of the craftsman.
    - wealth (float): The wealth of the craftsman.
    - utility_function (Utility): The utility function that represents the craftsman's preferences.
    - skill_level (int): The skill level of the craftsman.
    - projects (list): A list of the projects that the craftsman is working on.

    Methods:
    - produce_goods: Produces goods by hand.
    """
    def __init__(self, name,skill_level=None, age=None,wealth=None,utility_function=None):
        super().__init__(name, age,wealth,utility_function)
        self.skill_level = skill_level
        self.projects = []
    def produce_goods(self, project):
        """
        Produces goods by hand.
    
        Args:
        project (Project): The project to work on.
    
        Returns:
        float: The amount of goods produced.
        """
        # TODO: Implement the produce_goods method
        pass