class PonziScheme:
    """
    #### A Ponzi scheme is a fraudulent investment scheme that pays returns to earlier investors using the capital contributed
    by newer investors. The scheme relies on the recruitment of new investors to generate returns for existing investors
    and eventually collapses when there are not enough new investors to sustain it.

    Attributes:
        promise (str): The promise made to investors about the high returns they can expect to receive.
        victims (list): A list of victims who have invested in the scheme.

    Methods:
        add_victim(victim): Add a new victim to the scheme.
        get_info(): Display information about the scheme, including the promise and number of victims.
    """
    def __init__(self, promise):
        self.promise = promise
        self.victims = []
    def add_victim(self, victim):
        """
        Add a new victim to the Ponzi scheme.

        Args:
            victim (str): The name of the victim.
        """
        self.victims.append(victim)

    def get_info(self):
        """
        Display information about the Ponzi scheme, including the promise and number of victims.
        """
        print(f"Promise: {self.promise}")
        print(f"Number of victims: {len(self.victims)}")