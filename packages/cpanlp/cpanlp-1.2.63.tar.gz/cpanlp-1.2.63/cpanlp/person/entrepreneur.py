from cpanlp.person.consumer import *

class Entrepreneur(Consumer):
    """
    #### The Entrepreneur class represents a person who starts and runs a new business venture.
    
    Attributes:
    - name (str): The name of the entrepreneur.
    - company (str): The name of the company.
    - age (int): The age of the entrepreneur.
    - wealth (float): The wealth of the entrepreneur.
    - utility_function (Utility): The utility function that represents the entrepreneur's preferences.
    - experience (float): The years of experience of the entrepreneur.
    - entrepreneurship (float): The entrepreneur's level of entrepreneurship.
    - industry (str): The industry the entrepreneur operates in.
    - employees (list): A list of the entrepreneur's employees.

    Methods:
    - hire_employee: Hires an employee.
    - fire_employee: Fires an employee.
    - list_employees: Lists all employees.
    - raise_funds: Raises funds for the company.
    - acquire_company: Acquires another company.
    - take_risk: Takes a risk.
    - innovate: Innovates.
    - persist: Persists in the face of failure.
    - strive_for_excellence: Strives for excellence.
    """

    def __init__(self, name,company=None, age=None,wealth=None,utility_function=None,experience=None,entrepreneurship=None):
        super().__init__(name, age,wealth,utility_function)
        self.entrepreneurship=entrepreneurship
        self.experience = experience
        self.company = company
        self.industry = ""
        self.employees = []
    def hire_employee(self, employee):
        """
        Hires an employee.
    
        Args:
        employee (Employee): The employee to be hired.
        """
        self.employees.append(employee)
        print(f"{employee.name} has been hired by {self.company}.")
        
    def fire_employee(self, employee):
        """
        Fires an employee.
    
        Args:
        employee (Employee): The employee to be fired.
        """
        self.employees.remove(employee)
        print(f"{employee.name} has been fired by {self.company}.")
        
    def list_employees(self):
        """
        Lists all employees.
        """
        for employee in self.employees:
            print(employee.name)
            
    def raise_funds(self, amount):
        """
        Raises funds for the company.
    
        Args:
        amount (float): The amount of funds raised.
        """
        print(f"{self.company} has raised ${amount} in funding.")
        
    def acquire_company(self, company):
        """
        Acquires another company.
    
        Args:
        company (str): The name of the company to be acquired.
        """
        print(f"{self.company} has acquired {company.name}.")
        
    def take_risk(self, risk):
        """
        Takes a risk.
    
        Args:
        risk (float): The level of risk to be taken.
        """
        if risk > self.experience:
            print(self.name + " is taking a high risk.")
        else:
            print(self.name + " is taking a moderate risk.")
            
    def innovate(self):
        """
        Innovates.
        """
        print(self.name + " is constantly seeking new and innovative ideas.")
        
    def persist(self):
        """
        Persists in the face of failure.
        """
    def strive_for_excellence(self):
        print(self.name + " is always striving for excellence.")