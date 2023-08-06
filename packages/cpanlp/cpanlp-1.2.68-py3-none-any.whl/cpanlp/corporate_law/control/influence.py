from cpanlp.corporate_law.control.power import *
class SignificantInfluence(VotingPower):
    """
    Features:
    - Significant influence is the power to participate in the financial and operating policy decisions of another entity,but not the power to control those policies.
    """
    def __init__(self, name, voting_weight):
        super().__init__(name, voting_weight)
        if not 0.2 < self.voting_weight < 0.5 :
            raise ValueError("Significant Influence requires a voting weight between 20% and 50%")
    