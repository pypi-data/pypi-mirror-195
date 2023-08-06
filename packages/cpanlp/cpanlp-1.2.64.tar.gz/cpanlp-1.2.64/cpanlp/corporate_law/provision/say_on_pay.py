class SayOnPay:
    """
    #### Represents a Say-on-Pay provision, which is a provision that allows shareholders to vote on executive compensation.

    Args:
    - non_binding_vote: whether the vote is binding or non-binding on the company
    - frequency_of_vote: how often the vote is held, such as annually or every three years
    - disclosure_requirements: what information the company is required to disclose to shareholders about executive compensation
    - shareholder_engagement: how the company engages with shareholders about executive compensation

    Methods:
    - describe_say_on_pay: describes the Say-on-Pay provision
    """
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
    
    def update_disclosure_requirements(self, new_requirements):
        """
        Updates the disclosure requirements for executive compensation.

        Args:
        - new_requirements: the new disclosure requirements

        Returns:
        - N/A
        """
        self.disclosure_requirements = new_requirements

    def engage_with_shareholders(self, method):
        """
        Engages with shareholders about executive compensation.

        Args:
        - method: the method of engagement, such as town hall meetings or online forums

        Returns:
        - N/A
        """
        print(f"The company is engaging with shareholders about executive compensation using {method}.")