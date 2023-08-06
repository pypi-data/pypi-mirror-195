class Operation:
    """
    #### An Operation is a specific business activity or process, typically referring to a specific business function or department, such as production operation, sales operation, or customer service operation.
    Attributes:
    - name (str): The name of the operation.
    - description (str): A brief description of the operation.
    
    Methods:
    - perform(): Simulates the execution of the operation by printing a message indicating the name and description of the operation.

    """
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def perform(self):
        """
        Simulates the execution of the operation by printing a message indicating the name and description of the operation.
        """
        print(f"Performing operation '{self.name}': {self.description}")
