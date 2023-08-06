from cpanlp.corporate_law.contract.financial_instruments.bond import *
class SeniorNotes(Bond):
    """
    #### Senior notes are a type of debt security issued by a company or government agency. They are considered a type of
    bond, but with some unique features.

    Features:
    - Unsecured: Unlike traditional bonds, senior notes are unsecured, meaning they are not backed by any collateral.
      If the issuer defaults on the debt, the senior note holders have no claim to any specific assets, but are instead
      paid out of the issuer's general funds.
    - Senior in capital structure: Despite being unsecured, senior notes are considered senior in the issuer's capital
      structure. This means that in the event of a default, senior note holders have priority over other unsecured
      creditors, but are subordinate to secured creditors, such as bondholders or lenders who have a lien on specific
      assets.
    - Long-term maturity: Senior notes typically have a longer maturity than other types of debt, such as commercial
      paper or short-term notes.
    - Higher interest rate: Senior notes are typically offered at a higher interest rate to compensate for the higher
      risk to investors, as they lack collateral.

    Args:
        issuer (str): The name of the company or government agency issuing the senior notes.
        amount (float): The total amount of senior notes issued.
        maturity (int): The length of time until the senior notes reach maturity.

    Methods:
        get_issuer(): Returns the name of the issuer.
        get_amount(): Returns the total amount of senior notes issued.
        get_maturity(): Returns the length of time until the senior notes reach maturity.
        is_unsecured(): Returns True, indicating that the senior notes are unsecured.
        has_collateral(): Returns False, indicating that the senior notes lack collateral.
        get_priority(): Returns "Senior", indicating that the senior notes are senior in the issuer's capital structure.
        get_subordination(): Returns a string describing the senior notes' subordination to secured creditors and
            priority over other unsecured creditors.
        get_description(): Returns a string describing the key features of senior notes.
    """
    def __init__(self, issuer=None, amount=None,  maturity=None,parties=None,value=None, rate=None, currency=None,domestic=None,date=None,consideration=None, obligations=None,outstanding_balance=None):
        super().__init__(parties,value, rate, currency,domestic,date,consideration, obligations,outstanding_balance)
        self.issuer = issuer
        self.amount = amount
        self.maturity = maturity

    def get_issuer(self):
        return self.issuer

    def get_amount(self):
        return self.amount

    def get_maturity(self):
        return self.maturity

    def is_unsecured(self):
        return True

    def has_collateral(self):
        return False

    def get_priority(self):
        return "Senior"

    def get_subordination(self):
        return "Subordinate to secured creditors, but has priority over other unsecured creditors"

    def get_description(self):
        return "Senior notes are a type of unsecured bond that is subordinate to secured creditors, but has a higher priority than other unsecured creditors in the event of a default. They typically have a longer maturity than other types of debt and are offered at a higher interest rate to compensate for the lack of collateral."
