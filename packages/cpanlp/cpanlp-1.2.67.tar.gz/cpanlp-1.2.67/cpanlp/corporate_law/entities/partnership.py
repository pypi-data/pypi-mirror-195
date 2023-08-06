from cpanlp.corporate_law.entities.unincorporate import *

class Partnership(UnincorporatedEntity):
    """
    #### Represents a partnership
    Features:
    - unlimited liability: each partner is personally responsible for all debts and obligations of the partnership
    - personal risk: the amount of investment and liability that each partner personally bears
    - Continuity: the degree to which the partnership's existence is separate from that of its owners
    - partners: the individuals or entities that make up the partnership
    - general partners: partners who have unlimited liability and are actively involved in the management of the partnership
    - limited partners: partners who have limited liability and are not actively involved in the management of the partnership

    Args:
    - name: the name of the partnership
    - type: the type of entity, such as "corporation" or "LLC"
    - capital: the initial amount of capital invested in the partnership

    Methods:
    - add_partner: adds a partner to the partnership
    - remove_partner: removes a partner from the partnership
    - distribute_profit: distributes the partnership's profit among partners in a pre-agreed ratio
    - voting_procedure: conducts a voting procedure for major decisions on a given proposal
    - list_partners: lists all the partners of the partnership
    """
    def __init__(self, name,type=None,capital=None):
        super().__init__(name,type,capital)
        self.partners = []
        self.general_partners = []
        self.limited_partners=[]
    def add_partner(self, partner):
        """
        #### Adds a partner to the partnership.

        Args:
        - partner: the partner to be added

        Returns:
        - N/A
        """
        self.partners.append(partner)
    def remove_partner(self, partner):
        """
        #### Removes a partner from the partnership.

        Args:
        - partner: the partner to be removed

        Returns:
        - N/A
        """
        self.partners.remove(partner)
    def distribute_profit(self, profit):
        """Distribute the profit among partners in a pre-agreed ratio."""
        pass
    def voting_procedure(self,proposal):
        """Conduct voting procedure for major decisions on a given proposal"""
        print(f"Proposal: {proposal}")
        for partner in self.partners:
            vote = input(f"{partner}, do you approve this proposal (yes/no)")
            if vote.lower() not in ["yes","no"]:
                print("Invalid input")
            else:
                pass
    def list_partners(self):
        """List all the partners of the partnership"""
        print(self.partners)
        