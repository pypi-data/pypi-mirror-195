from cpanlp.corporate_law.entities.PLC import *
class ListedCompany(PLC):
    """
    #### Represents a public limited company that is publicly traded on a stock exchange, which has certain features and methods.

    Features:
    - limited liability: the owners' personal assets are generally protected from business debts and liabilities
    - personal risk: the amount of investment and liability that the owners personally bear
    - is_taxed: whether the entity is subject to taxation
    - Continuity: the degree to which the entity's existence is separate from that of its owners
    - publicly traded: the shares of the company are traded on a public stock exchange
    - shareholders: the individuals or entities that own shares in the company

    Args:
    - name: the name of the public limited company
    - type: the type of entity, such as "corporation" or "LLC"
    - capital: the initial amount of capital invested in the entity

    """
    def __init__(self,name,type=None,capital=None):
        super().__init__(name,type,capital)
        self.shareholders=[]
    def add_shareholder(self, shareholder):
        """
        Adds a shareholder to the ListedCompany.

        Args:
        - shareholder: the individual or entity to be added as a shareholder
        """
        self.shareholders.append(shareholder)

    def remove_shareholder(self, shareholder):
        """
        Removes a shareholder from the ListedCompany.

        Args:
        - shareholder: the individual or entity to be removed as a shareholder
        """
        if shareholder in self.shareholders:
            self.shareholders.remove(shareholder)

    def get_shareholders(self):
        """
        Returns the list of shareholders in the ListedCompany.

        Returns:
        - a list of shareholders
        """
        return self.shareholders