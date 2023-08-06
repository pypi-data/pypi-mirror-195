from cpanlp.financialmanagement.incentive.incentive import *

class PromotionIncentive(Incentive):
    """
    #### A promotion incentive is a type of incentive that encourages employees to work towards meeting certain performance criteria in order to receive a promotion. This class extends the Incentive class and includes additional functionality for evaluating officials based on performance criteria and promoting officials who meet certain criteria.
    
    Features:
    - officials: a list of officials who are eligible for the promotion incentive
    - performance_criteria: a dictionary to store performance criteria for each official
    - promotion_criteria: a dictionary to store promotion criteria for each official
    - promotion_results: a dictionary to store promotion results for each official
    
    Args:
    - officials: a list of officials who are eligible for the promotion incentive
    - type: the type of incentive
    - amount: the amount of the incentive
    - recipients: a list of recipients who will receive the incentive
    
    Methods:
    - set_performance_criteria: sets the performance criteria for a given official
    - set_promotion_criteria: sets the promotion criteria for a given official
    - evaluate_officials: evaluates officials based on their performance and sets their promotion results
    - promote_officials: promotes officials who meet the promotion criteria
    """
    def __init__(self, officials,type, amount, recipients):
        super().__init__(type, amount, recipients)
        self.officials = officials
        self.performance_criteria = {}  # a dictionary to store performance criteria for each official
        self.promotion_criteria = {}  # a dictionary to store promotion criteria for each official
        self.promotion_results = {}  # a dictionary to store promotion results for each official

    def set_performance_criteria(self, official, criteria):
        """Set the performance criteria for a given official."""
        self.performance_criteria[official] = criteria

    def set_promotion_criteria(self, official, criteria):
        """Set the promotion criteria for a given official."""
        self.promotion_criteria[official] = criteria

    def evaluate_officials(self):
        """Evaluate officials based on their performance and set their promotion results."""
        for official in self.officials:
            performance_score = self.performance_criteria[official]()
            if performance_score >= self.promotion_criteria[official]:
                self.promotion_results[official] = True
            else:
                self.promotion_results[official] = False

    def promote_officials(self):
        """Promote officials who meet the promotion criteria."""
        for official in self.officials:
            if self.promotion_results[official]:
                # do something to promote the official, such as increasing salary or giving a new job title
                pass


