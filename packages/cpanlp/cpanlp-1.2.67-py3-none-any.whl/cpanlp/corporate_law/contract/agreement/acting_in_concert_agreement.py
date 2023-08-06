from cpanlp.corporate_law.contract.agreement.agreement import *

class ActingInConcertAgreement(Agreement):
    """
    #### A class representing an acting in concert agreement between parties.
    #### An acting in concert agreement is a legal agreement between two or more parties in which they agree to coordinate their actions and vote together on certain matters related to a company or asset.
    Attributes:
    - parties (list[str]): A list of parties involved in the acting in concert agreement.
    - purpose (str): The purpose of the acting in concert agreement.
    - terms (str): The terms and conditions of the acting in concert agreement.
    - consensus_method (str): The consensus method used for decision-making in the acting in concert agreement.
    """
    def __init__(self, parties=None, purpose=None, terms=None, consensus_method=None):
        super().__init__(parties, purpose, terms)
        self.consensus_method = consensus_method