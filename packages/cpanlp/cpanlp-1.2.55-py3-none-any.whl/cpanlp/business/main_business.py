from cpanlp.business.business import *

class MainBusiness(Business):
    """
    #### A MainBusiness is a type of Business that specializes in providing a main service or product.
    Attributes:
    - name (str): The name of the main business.
    - industry (str): The industry in which the main business operates.
    - main_service (str): The main service or product offered by the main business.
    
    Methods:
    - description() -> str: Returns a description of the main business.
    """
    def __init__(self, name, industry, main_service):
        super().__init__(name, industry)
        self.main_service = main_service

    def description(self):
        """
        Returns a description of the main business.
        """
        return f"{self.name} is a business in the {self.industry} industry. " \
               f"Their main service is {self.main_service}."