class Team:
    """
    #### A class representing a team with a name, members, and a leader.
    Args:
    - name (str): The name of the team.
    - members (list): A list of team members (default is None).
    - leader (str): The name of the team leader (default is None).
    """
    def __init__(self, name, members = None, leader = None):
        self.name = name
        self.members = members if members is not None else []
        self.leader = leader