from cpanlp.corporate_law.contract.contract import *


class PurchaseContract(Contract):
    """
    Features:
    - A purchase contract is an agreement between a buyer and a seller for the sale and purchase of goods or services.
    It includes details such as the items being sold, the price, delivery terms, payment terms, and warranties.
    
    Args:
    - supplier: the party selling the goods or services
    - items: a list of items being purchased
    - price: the total price of the purchase
    - parties: a list of parties involved in the contract
    - consideration: the consideration being exchanged in the contract
    - obligations: the obligations of the parties in the contract
    """
    def __init__(self, supplier, items, price, parties=None, consideration=None, obligations=None):
        super().__init__(parties, consideration, obligations)
        self.supplier = supplier
        self.items = items
        self.price = price
