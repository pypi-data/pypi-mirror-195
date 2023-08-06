class Vote:
    """
    Features:
    - Types of vote: There are several types of votes in corporate law, including ordinary resolutions, special resolutions, and proxy votes. The type of vote required for a particular matter depends on the jurisdiction and the nature of the matter.

    - Voting thresholds: Voting thresholds refer to the percentage of votes required for a particular matter to be approved. In many jurisdictions, a simple majority (more than 50% of votes) is required for ordinary resolutions, while special resolutions may require a higher percentage, such as two-thirds or three-quarters of votes.
    
    - Voting procedures: Voting procedures refer to the rules and processes for conducting a vote. These may include the timing and location of the vote, the methods for casting and counting votes, and the requirements for quorum (the minimum number of shareholders or directors required to conduct a valid vote).
    
    - Shareholder rights: Shareholders have certain rights related to voting, such as the right to inspect voting records, the right to propose resolutions, and the right to participate in annual meetings.
    """
    def __init__(self, vote_type, voting_threshold, voting_procedures, shareholder_rights):
        self.vote_type = vote_type
        self.voting_threshold = voting_threshold
        self.voting_procedures = voting_procedures
        self.shareholder_rights = shareholder_rights
    
    def describe_vote(self):
        print("Vote type: ", self.vote_type)
        print("Voting threshold: ", self.voting_threshold)
        print("Voting procedures: ", self.voting_procedures)
        print("Shareholder rights: ", self.shareholder_rights)
