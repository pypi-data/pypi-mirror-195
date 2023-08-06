from cpanlp.department.department import *
class BoardOfDirectors(Department):
    """
    #### The class BoardOfDirectors is a subclass of the Department class and represents the board of directors in a company. The board of directors is responsible for making important decisions about the company's strategy, financials, management structure, and other key areas of the business.
    
    Attributes:
    
    - name (str): The name of the board of directors.
    - goals (list of str): The goals of the board of directors.
    - incentives (list of str): The incentives for the board of directors.
    
    Methods:
    
    - call_shareholders_meeting(): Call a meeting with the shareholders.
    - report_to_shareholders(): Report on the work of the board to the shareholders.
    - execute_shareholders_resolutions(): Execute the resolutions passed by the shareholders.
    - decide_on_business_plan(): Decide on the company's business plan and investment strategy.
    - formulate_annual_budget(): Formulate the company's annual financial budget.
    - formulate_profit_distribution(): Formulate the company's profit distribution plan and plan to make up for losses.
    - formulate_capital_increase_or_decrease(): Formulate the company's plan for increasing or decreasing registered capital and issuing bonds.
    - formulate_merger_plan(): Formulate the company's plan for merger, separation, dissolution or change of corporate form.
    - decide_on_internal_management(): Decide on the setting of the company's internal management structure.
    - hire_or_dismiss_manager(): Decide on the hiring or dismissal of the company manager and their compensation, and based on the manager's nomination, decide on the hiring or dismissal of the company's vice manager, financial officer and their compensation.
    - formulate_basic_management_system(): Formulate the company's basic management system.
    - other_responsibilities(): Other responsibilities as specified in the company's bylaws.

    """
    def __init__(self,name, goals=None, incentives=None):
        super().__init__(name, goals, incentives)
    def call_shareholders_meeting(self):
        pass
    def report_to_shareholders(self):
        """Report on the work of the board to shareholders"""
        pass
    def execute_shareholders_resolutions(self):
        """Execute resolutions passed by shareholders"""
        pass
    def decide_on_business_plan(self):
        """Decide on the company's business plan and investment strategy"""
        pass
    def formulate_annual_budget(self):
        """Formulate the company's annual financial budget"""
        pass
    def formulate_profit_distribution(self):
        """Formulate the company's profit distribution plan and plan to make up for losses"""
        pass
    def formulate_capital_increase_or_decrease(self):
        """Formulate the company's plan for increasing or decreasing registered capital and issuing bonds"""
        pass
    def formulate_merger_plan(self):
        """Formulate the company's plan for merger, separation, dissolution or change of corporate form"""
        pass
    def decide_on_internal_management(self):
        """Decide on the setting of the company's internal management structure"""
        pass
    def hire_or_dismiss_manager(self):
        """Decide on the hiring or dismissal of the company manager and their compensation, and based on the 
manager's nomination, decide on the hiring or dismissal of the company's vice manager, financial officer and 
their compensation"""
        pass
    
    def formulate_basic_management_system(self):
        """Formulate the company's basic management system"""
        pass
    def other_responsibilities(self):
        """Other responsibilities as specified in the company's bylaws"""
        pass