class ClawbackProvisions:
    """
 Clawback provisions in corporate law are provisions that allow a company to reclaim executive compensation in certain circumstances. Here are some key features of clawback provisions:

Triggers for clawback: Clawback provisions typically specify the circumstances under which executive compensation can be clawed back, such as accounting restatements due to material noncompliance with financial reporting requirements, misconduct or fraud by the executive, or failure to meet performance targets.
Types of compensation subject to clawback: Clawback provisions may apply to various types of executive compensation, including salary, bonus, stock options, and other incentives.
Timeframe for clawback: Clawback provisions may specify the timeframe within which the company can reclaim executive compensation, such as within a certain number of years after the triggering event.
Procedures for clawback: Clawback provisions may include procedures for the company to follow when invoking the provision, such as notifying the executive and allowing them to contest the clawback.   
    """
    def __init__(self, triggers_for_clawback, types_of_compensation_subject_to_clawback, timeframe_for_clawback, procedures_for_clawback):
        self.triggers_for_clawback = triggers_for_clawback
        self.types_of_compensation_subject_to_clawback = types_of_compensation_subject_to_clawback
        self.timeframe_for_clawback = timeframe_for_clawback
        self.procedures_for_clawback = procedures_for_clawback
    
    def describe_clawback_provisions(self):
        print("Triggers for clawback: ", self.triggers_for_clawback)
        print("Types of compensation subject to clawback: ", self.types_of_compensation_subject_to_clawback)
        print("Timeframe for clawback: ", self.timeframe_for_clawback)
        print("Procedures for clawback: ", self.procedures_for_clawback)
