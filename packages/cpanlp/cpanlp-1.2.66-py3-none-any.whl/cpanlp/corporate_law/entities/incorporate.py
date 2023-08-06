from cpanlp.corporate_law.entities.entity import *
class IncorporatedEntity(LegalEntity):
    """
    #### Represents a legal entity that has been incorporated, such as a corporation
    Features:
    - limited liability: the owners' personal assets are generally protected from business debts and liabilities
    - personal risk: the amount of investment and liability that the owners personally bear
    - is_taxed: whether the entity is subject to taxation
    - Continuity: the degree to which the entity's existence is separate from that of its owners
    
    Args:
    - name: the name of the incorporated entity
    - type: the type of entity, such as "corporation" or "LLC"
    - capital: the initial amount of capital invested in the entity
    """
    def __init__(self, name, type=None,capital=None):
        super().__init__(name, type,capital)
        self.limited_liability = True
        self.personal_risk = min(self.investment, self.liability)
        self.is_taxed=True
        self.Continuity = "High"