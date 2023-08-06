from cpanlp.corporate_law.entities.LLC import *
class SME(LLC):
    """
    #### Represents a small or medium-sized enterprise (SME), which is a type of LLC that has certain features and methods.

    Features:
    - limited liability: the owners' personal assets are generally protected from business debts and liabilities
    - personal risk: the amount of investment and liability that the owners personally bear
    - is_taxed: whether the entity is subject to taxation
    - Continuity: the degree to which the entity's existence is separate from that of its owners
    - shareholders: the individuals or entities that own shares in the company
    - public_accountability: whether the company is subject to public accountability and disclosure requirements

    Args:
    - name: the name of the SME
    - type: the type of entity, such as "corporation" or "LLC"
    - capital: the initial amount of capital invested in the SME

    Methods:
    - add_shareholder: adds a shareholder to the SME
    - remove_shareholder: removes a shareholder from the SME
    - list_shareholders: lists all the shareholders of the SME
    """
    def __init__(self, name,type,capital):
        super().__init__(name,type,capital)
        self.public_accountability=False