from cpanlp.corporate_law.contract.contract import *
class LaborContract(Contract):
    """
    Features:
    #### A labor contract is a type of contract that outlines the terms and conditions of employment between an employee and an employer. It typically includes details such as job duties, compensation, benefits, work hours, and employment duration.
    Args:
    - employee: the person who is being hired
    - employer: the company or organization that is hiring the employee
    - parties: a list of parties involved in the contract
    - consideration: the compensation or benefits provided to the employee in exchange for their work
    - obligations: the duties and responsibilities of the employee and employer under the contract
    - salary: the amount of money paid to the employee for their work

    """
    accounts = []
    def __init__(self,employee=None,employer=None, parties=None, consideration=None,obligations=None,salary=None):
        super().__init__(parties, consideration,obligations)
        self.employee = employee
        self.employer = employer
        self.salary = salary
        LaborContract.accounts.append(self)