class Capacity:
    """
    #### A Capacity object represents the maximum and current capacity of a resource or system.
    Attributes:
    - maximum_capacity (int): The maximum capacity of the resource or system.
    - current_capacity (int): The current capacity of the resource or system.
    
    Methods:
    - is_saturated() -> bool: Returns True if the current capacity is equal to or greater than the maximum capacity, False otherwise.
    """
    def __init__(self, maximum_capacity, current_capacity):
        self.maximum_capacity = maximum_capacity
        self.current_capacity = current_capacity
    @property
    def is_saturated(self):
        """
        Returns True if the current capacity is equal to or greater than the maximum capacity, False otherwise.
        """
        return self.current_capacity >= self.maximum_capacity