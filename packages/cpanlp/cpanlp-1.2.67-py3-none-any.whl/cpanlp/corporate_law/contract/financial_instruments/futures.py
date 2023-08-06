from cpanlp.corporate_law.contract.financial_instruments.financial_instrument import *
class Futures(FinancialInstrument):
    """
    #### A class representing a futures financial instrument.
    
    Attributes:
    - parties (list[str]): A list of parties involved in the futures agreement.
    - consideration (str): The consideration for the futures agreement.
    - obligations (str): The obligations for the futures agreement.
    - value (float): The monetary value of the futures agreement.
    - symbol (str): The symbol or code for the futures.
    - price (float): The price of the futures.
    - expiration_date (str): The expiration date of the futures.
    - underlying_asset (str): The underlying asset for the futures.
    - contract_size (int): The quantity of the futures contract.
    - tick_size (float): The minimum price fluctuation for the futures.
    - tick_value (float): The value of the minimum price fluctuation for the futures.
    """
    def __init__(self, symbol=None, price=None, expiration_date=None, underlying_asset=None, contract_size=None, tick_size=None, tick_value=None,parties=None, consideration=None,obligations=None, value=None):
        super().__init__(parties, consideration,obligations, value)
        self.symbol = symbol
        self.price = price
        self.expiration_date = expiration_date
        self.underlying_asset = underlying_asset
        self.contract_size = contract_size
        self.tick_size = tick_size
        self.tick_value = tick_value
#symbol：期货的代码或符号。
#price：期货的价格。
#expiration_date：期货的到期日期。
#underlying_asset：期货所对应的标的资产。
#contract_size：期货合约的数量。
#tick_size：期货价格波动的最小单位。
#tick_value：期货价格波动的最小单位对应的价值。
