class Arrangement:
    """
    #### Arrangement is a term used to describe an informal, non-binding agreement or understanding between two or more parties.

    Features:
    - Non-binding: Arrangements are not legally binding and do not have the force of law.
    - Informal: Arrangements are typically made through informal discussions or negotiations between the parties, and are
      not typically documented in a formal written agreement.
    - Purpose: Arrangements are made for a specific purpose or goal, which is usually described in general terms.
    - Terms: Arrangements may have some general terms or conditions that are agreed upon by the parties, but these are not
      typically as detailed or specific as those in a formal agreement.
    - Enforceability: Arrangements are not legally enforceable, although the parties may still be expected to adhere to
      the terms they have agreed upon.

    Args:
        parties (list): The parties involved in the arrangement.
        purpose (str): The purpose or goal of the arrangement.
        terms (str): Any general terms or conditions that are agreed upon by the parties.

    Methods:
        None
    """
    def __init__(self, parties=None, purpose=None, terms=None):
        self.parties = parties
        self.purpose = purpose
        self.terms = terms
        self.enforceability = False