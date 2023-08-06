from cpanlp.corporate_law.contract.financial_instruments.financial_instrument import *

class PrivateEquity(FinancialInstrument):
    """
    #### Private equity refers to a type of investment that is made in privately held companies, rather than publicly traded companies. Private equity investments can take many forms, but they all involve providing capital to a private company in exchange for an ownership stake in the company.

    Features:
    - Long-term focus: Private equity investments are typically made with a long-term perspective, and investors are
      willing to wait several years to see returns on their investment.
    - Active involvement: Private equity investors often take an active role in the companies they invest in, providing
      strategic guidance, support, and expertise to help the companies grow and succeed.
    - High risk, high reward: Private equity investments are typically considered to be high-risk investments, as they
      are made in companies that are not publicly traded and are not subject to the same level of regulatory oversight
      as publicly traded companies. However, the potential rewards from private equity investments can also be much
      higher than those from more traditional investments.
    - Limited liquidity: Private equity investments are often illiquid, meaning that the investors' capital is tied up
      for a long period of time and cannot be easily sold or transferred.
    - Due diligence: Before making a private equity investment, investors typically perform extensive due diligence to
      evaluate the company, its management team, and its financial and operational performance.
    - Limited transparency: Private companies are not subject to the same reporting and disclosure requirements as
      publicly traded companies, so private equity investors often have limited information about the financial
      performance and operations of the companies they invest in.

    Args:
        company (str): The name of the private company.
        investment_amount (float): The amount of capital invested in the company.
        investment_period (int): The length of the investment period in years.
        involvement (bool): Whether the investor is actively involved in the company.
        risk (bool): Whether the investment is considered high-risk.
        liquidity (bool): Whether the investment is liquid or illiquid.
        due_diligence (bool): Whether due diligence was performed before making the investment.

    Methods:
        describe(): Prints a description of the private equity investment.
    """

    def __init__(self, company=None, investment_amount=None, investment_period=None, involvement=None, risk=None, liquidity=None, due_diligence=None,parties=None, consideration=None,obligations=None, value=None):
        super().__init__(parties, consideration,obligations, value)
        self.company = company
        self.investment_amount = investment_amount
        self.investment_period = investment_period
        self.involvement = involvement
        self.risk = risk
        self.liquidity = liquidity
        self.due_diligence = due_diligence

    def describe(self):
        print("Company: {}".format(self.company))
        print("Investment amount: {}".format(self.investment_amount))
        print("Investment period: {} years".format(self.investment_period))
        print("Involvement: {}".format("Active" if self.involvement else "Passive"))
        print("Risk level: {}".format("High" if self.risk else "Low"))
        print("Liquidity: {}".format("Limited" if self.liquidity else "Flexible"))
        print("Due diligence: {}".format("Performed" if self.due_diligence else "Not performed"))

