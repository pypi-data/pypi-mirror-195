class SayOnPay:
    def __init__(self, non_binding_vote, frequency_of_vote, disclosure_requirements, shareholder_engagement):
        self.non_binding_vote = non_binding_vote
        self.frequency_of_vote = frequency_of_vote
        self.disclosure_requirements = disclosure_requirements
        self.shareholder_engagement = shareholder_engagement
    
    def describe_say_on_pay(self):
        print("Non-binding vote: ", self.non_binding_vote)
        print("Frequency of vote: ", self.frequency_of_vote)
        print("Disclosure requirements: ", self.disclosure_requirements)
        print("Shareholder engagement: ", self.shareholder_engagement)
