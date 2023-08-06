class Acquisition:
    """
    #### Represents an acquisition transaction between a target company and an acquiring company.
    Attributes:
    - target_company (str): the name of the target company
    - acquisition_ratio (float): the percentage of the target company's shares acquired by the acquiring company
    - acquiring_company (str): the name of the acquiring company
    - price (float): the amount paid by the acquiring company to acquire the target company
    - leverage_ratio (float): the ratio of debt to equity used to finance the acquisition
    - date (str): the date of the acquisition transaction
    """
    def __init__(self, target_company, acquiring_company, acquisition_ratio=None,price=None,leverage_ratio=None,date=None):
        self.target_company = target_company
        self.acquisition_ratio = acquisition_ratio
        self.acquiring_company = acquiring_company
        self.price = price
        self.leverage_ratio = leverage_ratio
        self.date = date