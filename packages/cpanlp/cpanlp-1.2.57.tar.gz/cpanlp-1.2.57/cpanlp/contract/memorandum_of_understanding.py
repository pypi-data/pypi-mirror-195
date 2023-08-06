from typing import List

class MOU:
    """
    Features:
        A memorandum of understanding (MOU) is a non-binding agreement between two or more parties that outlines a 
        shared understanding of goals and expectations for a future collaboration or partnership. MOUs are commonly used in business, government, and other fields to establish a framework for further negotiations or to outline the terms of a proposed agreement.

    Args:
    - parties (list): A list of the parties involved in the MOU.
    - purpose (str): A description of the purpose of the MOU and the goals it aims to achieve.
    - terms (dict): A dictionary containing the specific terms and conditions of the MOU, including any deadlines, performance metrics, or other requirements.

    Methods:
    - set_enforceability(enforceable: bool) -> None:Set the enforceability of the MOU to either True or False.
    - get_parties() -> List[str]:Return a list of the parties involved in the MOU.
    - get_purpose() -> str:Return a description of the purpose of the MOU.
    - get_terms() -> dict:Return a dictionary containing the specific terms and conditions of the MOU.
    - is_enforceable() -> bool:Return whether the MOU is enforceable or not.
    """
    def __init__(self, parties=None, purpose=None, terms=None):
        self.parties = parties if parties is not None else []
        self.purpose = purpose if purpose is not None else ""
        self.terms = terms if terms is not None else {}
        self.enforceability = False

    def set_enforceability(self, enforceable: bool) -> None:
        """
        Set the enforceability of the MOU to either True or False.
        """
        self.enforceability = enforceable

    def get_parties(self) -> List[str]:
        """
        Return a list of the parties involved in the MOU.
        """
        return self.parties

    def get_purpose(self) -> str:
        """
        Return a description of the purpose of the MOU.
        """
        return self.purpose

    def get_terms(self) -> dict:
        """
        Return a dictionary containing the specific terms and conditions of the MOU.
        """
        return self.terms

    def is_enforceable(self) -> bool:
        """
        Return whether the MOU is enforceable or not.
        """
        return self.enforceability