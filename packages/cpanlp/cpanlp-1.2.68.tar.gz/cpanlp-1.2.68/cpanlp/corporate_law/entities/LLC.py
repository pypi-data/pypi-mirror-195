from cpanlp.corporate_law.entities.incorporate import *
from datetime import timedelta, date
import random
class LLC(IncorporatedEntity):
    """
    #### Represents a limited liability company, which has certain features and methods.

    Features:
    - limited liability: the owners' personal assets are generally protected from business debts and liabilities
    - personal risk: the amount of investment and liability that the owners personally bear
    - is_taxed: whether the entity is subject to taxation
    - Continuity: the degree to which the entity's existence is separate from that of its owners
    - goods: the goods or services produced or offered by the company
    - monopoly: whether the company has a temporary monopoly on a particular good or service
    - monopoly_start: the date on which the monopoly started
    - monopoly_end: the date on which the monopoly will end
    - subsidiaries: the LLC's subsidiary companies
    - ownership: the LLC's ownership structure
    - control: the LLC's management and decision-making structure
    - shareholders: the individuals or entities that own shares in the LLC
    - board_members: the individuals who make up the LLC's board of directors
    - board_of_supervisors: the individuals who supervise the LLC's board of directors
    - independent_financial_advisor: an advisor who provides financial advice to the LLC
    - chairman: the individual who chairs the LLC's board of directors
    - main_business: the LLC's main line of business
    - previous_main_business: the LLC's previous main line of business

    Args:
    - name: the name of the LLC
    - type: the type of entity, such as "corporation" or "LLC"
    - capital: the initial amount of capital invested in the LLC

    Methods:
    - establish_subsidiary: creates a new subsidiary LLC
    - transfer_assets: transfers assets to a subsidiary LLC
    - innovate: simulates the innovation process and gives the LLC a temporary monopoly on a particular good or service
    - lose_monopoly: ends the LLC's temporary monopoly
    - check_monopoly: checks whether the LLC still has a temporary monopoly
    - imitate_product: imitates a product from another company
    """
    def __init__(self, name,type=None,capital=None):
        super().__init__(name,type,capital)
        self.goods = []
        self.monopoly = False
        self.monopoly_start = None
        self.monopoly_end = None
        self.subsidiaries = []
        self.ownership = None
        self.control = None
        self.shareholders = []
        self.board_members = []
        self.board_of_supervisors = []
        self.independent_financial_advisor = None
        self.chairman = None
        self.main_business = None
        self.previous_main_business = None
    @property
    def main_business_has_changed(self):
        return self.main_business != self.previous_main_business

    def establish_subsidiary(self, subsidiary_name, subsidiary_type, subsidiary_capital):
        """
        #### Creates a new subsidiary LLC and adds it to the parent LLC's list of subsidiaries.

        Args:
        - subsidiary_name: the name of the subsidiary LLC
        - subsidiary_type: the type of entity, such as "corporation" or "LLC"
        - subsidiary_capital: the initial amount of capital invested in the subsidiary LLC

        Returns:
        - the newly created subsidiary LLC
        """
        subsidiary = LLC(subsidiary_name, subsidiary_type,subsidiary_capital)
        self.subsidiaries.append(subsidiary)
        return subsidiary
    def transfer_assets(self, subsidiary, assets):
        """
        #### Transfers assets from the parent LLC to a subsidiary LLC.

        Args:
        - subsidiary: the subsidiary LLC to which the assets will be transferred
        - assets: a list of assets to be transferred

        Returns:
        - a message confirming the successful transfer of the assets
        """
        if subsidiary not in self.subsidiaries:
            raise ValueError(f"{subsidiary.name} is not a subsidiary of {self.name}")
        for asset in assets:
            if asset not in self.assets:
                raise ValueError(f"{asset} is not an asset of {self.name}")
            self.assets.remove(asset)
            subsidiary.assets.append(asset)
        return f"Assets {assets} are transferred to {subsidiary.name} successfully"
    def innovate(self,new_goods):
        """
        #### Simulates the innovation process and gives the LLC a temporary monopoly on a particular good or service.

        Args:
        - new_goods: the new good or service that the LLC has innovated

        Returns:
        - N/A
        """
        # simulate the innovation process
        self.new_good = new_goods
        self.goods.append(new_goods)
        self.monopoly = True
        self.monopoly_start = date.today()
        # random number of years for the monopoly to last (between 1 and 5)
        monopoly_years = random.randint(1, 5)
        self.monopoly_end = self.monopoly_start + timedelta(days=365*monopoly_years)
        print(f"{self.name} has innovated and now has a temporary monopoly on {new_goods} until {self.monopoly_end}.")
    def lose_monopoly(self):
        self.monopoly = False
        self.monopoly_start = None
        self.monopoly_end = None
        print(f"{self.name}'s monopoly has ended.")
    def check_monopoly(self):
        if self.monopoly and self.monopoly_end:
            if date.today() > self.monopoly_end:
                self.lose_monopoly()
            else:
                print(f"{self.name} still has a monopoly on {self.goods[-1]} until {self.monopoly_end}.")
        else:
            print(f"{self.name} does not currently have a monopoly.")
    def imitate_product(self, company, product):
        """
        #### Imitates a product from another company.

        Args:
        - company: the company from which the product will be imitated
        - product: the product that will be imitated

        Returns:
        - N/A
        """
        print(f"{self.name} is imitating {product} from {company}.")
    def add_shareholder(self, shareholder):
        """
        Adds a shareholder to the SME.

        Args:
        - shareholder: the shareholder to be added

        Returns:
        - N/A
        """
        self.shareholders.append(shareholder)

    def remove_shareholder(self, shareholder):
        """
        Removes a shareholder from the SME.

        Args:
        - shareholder: the shareholder to be removed

        Returns:
        - N/A
        """
        self.shareholders.remove(shareholder)

    def list_shareholders(self):
        """
        Lists all the shareholders of the SME.

        Args:
        - N/A

        Returns:
        - N/A
        """
        print(self.shareholders)
        