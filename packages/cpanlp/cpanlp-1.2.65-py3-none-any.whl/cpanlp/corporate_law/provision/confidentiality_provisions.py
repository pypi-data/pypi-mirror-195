class ConfidentialityProvisions:
    """
    #### Confidentiality provisions in corporate law are provisions that prohibit employees from sharing confidential information with third parties.
    Features:

    - Definition of confidential information: Confidentiality provisions typically define what constitutes confidential
    information, which may include trade secrets, proprietary information, customer lists, financial information, and other sensitive business information.
    - Obligations of employees: Confidentiality provisions require employees to keep confidential information confidential and to take reasonable steps to prevent unauthorized access or disclosure of such information.
    - Exceptions to confidentiality: Confidentiality provisions may include exceptions for certain situations, such as when disclosure is required by law or by a court order.
    - Consequences of breach: Confidentiality provisions may specify the consequences of breaching the provision, which may include termination of employment, civil liability, or criminal charges.
    
    Args:
    
    - definition_of_confidential_information: the definition of confidential information as defined in the provision
    obligations_of_employees: the obligations of employees to keep confidential information confidential and to take
    reasonable steps to prevent unauthorized access or disclosure of such information
    - exceptions_to_confidentiality: the exceptions to confidentiality, such as when disclosure is required by law or by a court order
    - consequences_of_breach: the consequences of breaching the provision, which may include termination of employment,
    civil liability, or criminal charges.
    
    Methods:
    
    - describe_confidentiality_provisions: a method that prints out the features of the confidentiality provisions
    """
    def __init__(self, definition_of_confidential_information, obligations_of_employees, exceptions_to_confidentiality, consequences_of_breach):
        self.definition_of_confidential_information = definition_of_confidential_information
        self.obligations_of_employees = obligations_of_employees
        self.exceptions_to_confidentiality = exceptions_to_confidentiality
        self.consequences_of_breach = consequences_of_breach
    
    def describe_confidentiality_provisions(self):
        print("Definition of confidential information: ", self.definition_of_confidential_information)
        print("Obligations of employees to keep confidential information confidential and to take reasonable steps to prevent unauthorized access or disclosure of such information: ", self.obligations_of_employees)
        print("Exceptions to confidentiality, such as when disclosure is required by law or by a court order: ", self.exceptions_to_confidentiality)
        print("Consequences of breaching the provision, which may include termination of employment, civil liability, or criminal charges: ", self.consequences_of_breach)
