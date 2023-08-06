class Business:
    """
    #### a business refers to the commercial activities and management practices of an enterprise, including marketing, strategic planning, financial management, etc., to achieve profitability and growth. 
    Attributes:
    - name (str): The name of the business.
    - industry (str): The industry in which the business operates.
    
    Methods:
    - description() -> str: Returns a description of the business.
    """
    def __init__(self, name, industry):
        self.name = name
        self.industry = industry

    def description(self):
        """
        #### Returns a description of the business.
        """
        return f"{self.name} is a business in the {self.industry} industry."
