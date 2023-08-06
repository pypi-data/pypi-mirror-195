from cpanlp.corporate_law.entities.entity import *

class Stakeholder(LegalEntity):
    """
    A stakeholder refers to any individual, group, or organization that has an interest or concern in the activities of a business. This can include shareholders, employees, customers, suppliers, the community, and even the environment.

    """
    def __init__(self, name,type=None,capital=None, interests=None,power=None):
        super().__init__(name,type,capital)
        self.name = name
        self.interests = interests
        self.power = power
        self.contact_info = ""
        self.concern=""
        self.suggest=""

def main():
    print("hello")
if __name__ == '__main__':
    main()