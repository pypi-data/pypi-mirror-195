from cpanlp.person.consumer import *

class ReportingPerson(Consumer):
    """
    #### A reporting person is an individual or company that reports information about insider trading activities of the company's executives and directors to the regulatory authorities, such as the Securities and Exchange Commission (SEC) in the United States.
    
    Attributes:
    - name: str, the name of the reporting person
    - age: int, the age of the reporting person
    - wealth: float, the wealth of the reporting person
    - utility_function: function, the utility function of the reporting person
    - share: float, the number of shares involved in the insider trading activity
    - company: str, the name of the company where the insider trading activity occurred
    - title: str, the job title of the executive or director involved in the insider trading activity
    - transaction_date: str, the date of the insider trading activity
    """
    def __init__(self, name,company=None, title=None, transaction_date=None,share=None, age=None,wealth=None,utility_function=None):
        super().__init__(name, age,wealth,utility_function)
        self.share = share
        self.company = company
        self.title=title
        self.transaction_date =transaction_date