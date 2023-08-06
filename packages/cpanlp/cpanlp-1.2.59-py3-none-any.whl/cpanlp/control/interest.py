class Interest:
    """
    #### An Interest object represents an investor's ownership stake in a business, which entitles the investor to a portion of the business's profits and assets.
    """
    def __init__(self, percent: float, type: str):
        """
        Initialize a new Interest object with a specified ownership percentage and type.

        Args:
            percent (float): The percentage of ownership in the business.
            type (str): The type of interest, such as equity or debt.

        Raises:
            ValueError: If the percentage is not between 0 and 100, or if the type is not a valid option.
        """
        if not 0 <= percent <= 100:
            raise ValueError("Percentage must be between 0 and 100")
        if type not in ["equity", "debt"]:
            raise ValueError("Invalid interest type")
        self.percent = percent 
        self.type = type
