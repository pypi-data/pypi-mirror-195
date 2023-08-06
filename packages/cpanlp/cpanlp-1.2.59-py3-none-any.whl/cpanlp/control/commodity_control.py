class CommodityControl:
    """
    #### A class representing the control of commodities and the recognition of income from their sale.
    Args:
    - owner (str): The owner of the commodities.
    Methods:
    - recognize_income(product_info: dict) -> bool: Determines whether income should be recognized from the sale of a commodity based on specific indicators of control, such as transfer of ownership or risk and reward.
    """
    def __init__(self,owner):
        self.owner=owner
    def __str__(self):
        return f"Control(owner={self.owner})"
    def recognize_income(self,product_info: dict = {'current_payment_obligation': True,'ownership_transferred': False,
    'physical_transfer': False,'risk_and_reward_transferred': False,'accepted_by_customer': False,
    'other_indicators_of_control': False}): 
        """
        #### Determines whether income should be recognized from the sale of a commodity based on specific indicators of control.
        Args:
            - product_info (dict): A dictionary of indicators of control, such as transfer of ownership or risk and reward.
        
        Returns:
            bool: True if income should be recognized, False otherwise.
        """
            #确认销售收入
    # 企业就该商品享有现时收款权利，即客户就该商品负有现时付款义务
        if product_info['current_payment_obligation']:
            return True# 企业已将该商品的法定所有权转移给客户，即客户已拥有该商品的法定所有权
        elif product_info['ownership_transferred']:
            return True# 企业已将该商品实物转移给客户，即客户已实物占有该商品
        elif product_info['physical_transfer']:
            return True# 企业已将该商品所有权上的主要风险和报酬转移给客户，即客户已取得该商品所有权上的主要风险和报酬
        elif product_info['risk_and_reward_transferred']:
            return True# 客户已接受该商品
        elif product_info['accepted_by_customer']:
            return True# 其他表明客户已取得商品控制权的迹象
        elif product_info['other_indicators_of_control']:
            return True# 其他情况均不确认销售收入
        else:
            return False