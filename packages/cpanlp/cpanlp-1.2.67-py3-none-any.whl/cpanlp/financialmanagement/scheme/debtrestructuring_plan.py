class DebtRestructuringPlan:
    """
    #### A class representing a plan to restructure debt.
    #### Debt restructuring is the process of renegotiating the terms of your debt so your payments are more manageable. This can include extending the repayment period, lowering the interest rate, or reducing the overall balance owed.
    Attributes:
    -----------
    name : str
        The name of the debt restructuring plan.
    amount : float
        The total amount of debt being restructured.
    terms : str
        The terms of the debt restructuring plan.
    creditors : list
        A list of creditors involved in the debt restructuring plan.

    Methods:
    --------
    display_info() -> None:
        Displays information about the debt restructuring plan.
    update_terms(new_terms: str) -> None:
        Updates the terms of the debt restructuring plan.
    add_creditor(creditor: str) -> None:
        Adds a creditor to the list of creditors involved in the debt restructuring plan.
    remove_creditor(creditor: str) -> None:
        Removes a creditor from the list of creditors involved in the debt restructuring plan.
    """

    def __init__(self, name, amount, terms, creditors):
        self.name = name
        self.amount = amount
        self.terms = terms
        self.creditors = creditors
        
    def display_info(self) -> None:
        """
        Displays information about the debt restructuring plan.
        """
        print("Debt Restructuring Plan:", self.name)
        print("Amount:", self.amount)
        print("Terms:", self.terms)
        print("Creditors:", self.creditors)

    def update_terms(self, new_terms: str) -> None:
        """
        Updates the terms of the debt restructuring plan.

        Parameters:
        -----------
        new_terms : str
            The new terms of the debt restructuring plan.
        """
        self.terms = new_terms

    def add_creditor(self, creditor: str) -> None:
        """
        Adds a creditor to the list of creditors involved in the debt restructuring plan.

        Parameters:
        -----------
        creditor : str
            The name of the creditor to be added.
        """
        self.creditors.append(creditor)

    def remove_creditor(self, creditor: str) -> None:
        """
        Removes a creditor from the list of creditors involved in the debt restructuring plan.

        Parameters:
        -----------
        creditor : str
            The name of the creditor to be removed.
        """
        self.creditors.remove(creditor)
