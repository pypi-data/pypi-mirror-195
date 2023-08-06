from cpanlp.corporate_law.entities.LLC import *
class PLC(LLC):
    """
    #### Represents a public limited company, which is a type of limited liability company that is publicly traded and has certain features and methods.
    
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
        self.publicly_traded = True