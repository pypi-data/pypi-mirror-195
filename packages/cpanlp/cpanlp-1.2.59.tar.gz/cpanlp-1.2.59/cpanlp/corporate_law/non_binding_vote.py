from cpanlp.corporate_law.vote import *

class NonBindingVote(Vote):
    """
    #### In corporate law, a non-binding vote refers to a vote that does not create a legal obligation, but rather 
    expresses the opinion or preference of the voters on a particular matter. Here are some key features of non-binding votes:
    
    Features:
    - Types of non-binding vote: There are several types of non-binding votes in corporate law, including advisory votes, straw polls, and indicative votes. The purpose of these votes is to provide guidance or feedback to the company, its management, or its shareholders, without creating a legal obligation.
    
    - Voting procedures: Non-binding votes may follow the same procedures as binding votes, such as the timing and location of the vote, the methods for casting and counting votes, and the requirements for quorum. However, the outcome of a non-binding vote is not legally enforceable.
    
    - Shareholder rights: Shareholders have the right to participate in non-binding votes, but the outcome of the vote does not create a legal obligation on the company or its management.
    
    - Effects of non-binding vote: While non-binding votes do not create a legal obligation, they can have practical effects on the company and its stakeholders. For example, a negative vote on executive compensation may lead to changes in the company's compensation policies or public relations strategy.
    """
    def __init__(self, vote_type, voting_procedures, shareholder_rights, effects_of_vote,voting_threshold):
        super().__init__(vote_type, voting_threshold, voting_procedures, shareholder_rights)
        self.vote_type = vote_type
        self.effects_of_vote = effects_of_vote
    
    def describe_non_binding_vote(self):
        print("Vote type: ", self.vote_type)
        print("Voting procedures: ", self.voting_procedures)
        print("Shareholder rights: ", self.shareholder_rights)
        print("Effects of vote: ", self.effects_of_vote)
