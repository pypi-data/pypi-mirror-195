from cpanlp.person.consumer import *
class Employee(Consumer):
    """
    The Employee class represents an employee of an organization.
    Attributes:
    - name (str): The name of the employee.
    - age (int): The age of the employee.
    - wealth (float): The wealth of the employee.
    - utility_function (Utility): The utility function that represents the employee's preferences.
    - emp_id (str): The employee's identification number.
    - salary (float): The employee's salary.
    - department (str): The department the employee works in.
    - job_title (str): The title of the employee's job.
    - experience (float): The years of experience of the employee.
    - education (str): The education level of the employee.

    Methods:
    - perform_job: Performs the duties of the employee's job.
    """
    def __init__(self, name, age=None,wealth=None,utility_function=None, salary=None, department=None):
        super().__init__(name, age,wealth,utility_function)
        self.emp_id = None
        self.salary = salary
        self.department = department
        self.job_title = None
        self.experience = None
        self.education = None
    def perform_job(self):
        """
        Performs the duties of the employee's job.
        """
        # TODO: Implement the perform_job method
        pass