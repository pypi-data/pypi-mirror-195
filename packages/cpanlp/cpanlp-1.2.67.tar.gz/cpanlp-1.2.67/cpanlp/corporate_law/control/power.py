class VotingPower:
    """
    #### A class representing voting power or interest in a business or accounting context. Voting power refers to the total number or percentage of votes entitled to be cast on an issue, excluding any contingent votes.
    
    Args:
        - name: A string representing the name of the entity holding the voting power
        - voting_weight: A float representing the voting weight or percentage of votes entitled to be cast
    """
    def __init__(self, name, voting_weight):
        self.name = name
        self.voting_weight = voting_weight
    def get_voting_power(self):
        return self.voting_weight
        