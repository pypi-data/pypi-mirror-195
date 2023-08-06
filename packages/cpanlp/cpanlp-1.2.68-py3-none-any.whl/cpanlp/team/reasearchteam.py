from cpanlp.team.team import *
class ResearchTeam(Team):
    """
    #### A class representing a research team with a name, an area of research,members, and a leader.
    Args:
        - name (str): The name of the research team.
        - area_of_research (str): The area of research of the team.
        - members (list): A list of team members (default is None).
        - leader (str): The name of the team leader (default is None).
    """
    def __init__(self, name,area_of_research, members=None,leader=None):
        Team.__init__(self, name, members,leader)
        self.area_of_research = area_of_research