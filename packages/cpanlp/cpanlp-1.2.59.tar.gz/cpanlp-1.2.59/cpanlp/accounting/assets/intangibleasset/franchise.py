from cpanlp.accounting.assets.intangibleasset.intangibleasset import *

class Franchise(IntangibleAsset):
    """
    #### A class representing franchise rights as an intangible asset.
    
    Args:
            brand: The brand associated with the franchise.
            products: The products associated with the franchise.
            services: The services associated with the franchise.
            training: The training provided by the franchisor to the franchisee.
            marketing: The marketing support provided by the franchisor to the franchisee.
            support: The technical support provided by the franchisor to the franchisee.
            date: The date the franchise rights were acquired, in the format "YYYY-MM-DD".
            amortization_period: The number of years over which to amortize the cost of the franchise rights.
    """
    def __init__(self, brand=None, products=None, services=None, training=None, marketing=None, support=None,account=None,debit=None, date=None,amortization_rate=None,amortization_period=None):
        super().__init__(account,debit, date,amortization_rate,amortization_period)

        self.brand = brand # 品牌
        self.products = products # 产品
        self.services = services # 服务
        self.training = training # 培训
        self.marketing = marketing # 市场营销
        self.support = support # 技术支持

    def provide_brand(self):
        """
        #### Provide brand sharing to the franchisee.
        """
        pass

    def standardize_operations(self):
        """
        #### Standardize the franchisee's operations according to the franchisor's guidelines.
        """
        pass

    def provide_support(self):
        """
        #### Provide comprehensive management support to the franchisee.
        """
        pass

    def collect_fees(self):
        """
        #### Collect authorization fees, management fees, and other fees from the franchisee.
        """
        pass
    def __repr__(self) -> str:
        return f"Franchise(brand={self.brand}, products={self.products}, services={self.services}, " \
               f"training={self.training}, marketing={self.marketing}, support={self.support}, " \
               f"date={self.date})"





