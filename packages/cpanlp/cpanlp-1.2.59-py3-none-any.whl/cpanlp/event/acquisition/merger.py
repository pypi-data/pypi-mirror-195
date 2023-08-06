class Merger:
    """
    #### The Merger class represents the merging of two companies into a single new company. 

    Attributes:
    - target_company (str): the name of the company being merged into the acquiring company
    - acquiring_company (str): the name of the company doing the acquiring
    - merger_price (float): the cost of the merger, if any
    - date (datetime): the date of the merger
    """
    def __init__(self, target_company, acquiring_company, merger_price=None, date=None):
        self.target_company = target_company
        self.acquiring_company = acquiring_company
        self.merger_price = merger_price
        self.date = date
