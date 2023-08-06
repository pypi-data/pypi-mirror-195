from cpanlp.corporate_law.entities.entity import *
class UnincorporatedEntity(LegalEntity):
    """
    #### Represents an unincorporated entity, which has certain features and methods.

    Features:
    - unlimited liability: the owners' personal assets are not protected from business debts and liabilities
    - personal risk: the amount of investment and liability that the owners personally bear
    - is_taxed: whether the entity is subject to taxation
    - Continuity: the degree to which the entity's existence is separate from that of its owners

    Args:
    - name: the name of the unincorporated entity
    - type: the type of entity, such as "corporation" or "LLC"
    - capital: the initial amount of capital invested in the entity

    Methods:
    - N/A
    """
    def __init__(self, name, type=None,capital=None):
        super().__init__(name, type,capital)
        self.limited_liability = False
        self.personal_risk = max(self.investment, self.liability)
        self.is_taxed=False
        self.Continuity = "low"