from cpanlp.business.activity import *
from typing import List
class ValueChain:
    """
    #### A value chain is a series of activities or processes that a company uses to create value for its customers.Each activity in the value chain adds value to the product or service that the company is providing.
    
    Features:
    - activities: a list of Activity objects that make up the value chain
    
    Args:
    - activities: a list of Activity objects that make up the value chain
    
    Methods:
    - add_activity(activity: Activity) -> None: adds an Activity object to the value chain
    - remove_activity(activity: Activity) -> None: removes an Activity object from the value chain
    - get_activities() -> List[Activity]: returns the list of Activity objects in the value chain
    - get_value() -> float: calculates and returns the total value added by all activities in the value chain
    """
    def __init__(self, activities: List[Activity]):
        self.activities = activities

    def add_activity(self, activity: Activity):
        self.activities.append(activity)

    def remove_activity(self, activity: Activity):
        self.activities.remove(activity)

    def get_activities(self):
        return self.activities

    def get_value(self):
        """
        #### Calculates the total value added by all activities in the value chain.
        """
        value = 0
        for activity in self.activities:
            value += activity.get_value_added()
        return value
