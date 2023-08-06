from cpanlp.person.consumer import *

class Partner(Consumer):
    """
    #### The class Partner represents a consumer who is a partner in a partnership.
    
    Attributes:
    
    - name: a string representing the name of the partner
    - age: an integer representing the age of the partner
    - wealth: a float representing the wealth of the partner
    - utility_function: a function representing the utility function of the partner
    - share: a float representing the share of the partner in the partnership
    """
    def __init__(self, name,share=None, age=None,wealth=None,utility_function=None):
        super().__init__(name, age,wealth,utility_function)
        self.share = share