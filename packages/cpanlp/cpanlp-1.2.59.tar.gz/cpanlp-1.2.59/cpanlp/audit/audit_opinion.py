from cpanlp.audit.audit import *

class AuditOpinion(Audit):
    """
    #### A class to represent the audit opinion of a company's financial statements.
    #### In accounting, an audit opinion is a statement issued by an auditor after reviewing a company's financial statements and internal controls.
    Features:
    - Types of audit opinion: There are several types of audit opinions, including unqualified, 
    qualified, adverse, and disclaimer. An unqualified opinion indicates that the financial statements 
    are fairly presented in all material respects, while the other types indicate varying degrees of 
    concern about the accuracy or completeness of the financial statements.
    - Basis for opinion: Audit opinions are based on the auditor's review of the company's financial 
    statements, internal controls, and other relevant information. The auditor's opinion is intended 
    to provide reasonable assurance that the financial statements are free from material misstatement, 
    whether due to fraud or error.
    - Reporting format: Audit opinions are typically presented in a standard format, including an 
    introductory paragraph, a scope paragraph, an opinion paragraph, and an explanatory paragraph if 
    necessary.
    - Effects of opinion: The auditor's opinion can have significant effects on the company and its 
    stakeholders, including investors, lenders, and regulators. For example, a qualified or adverse 
    opinion may lead to lower investor confidence or increased regulatory scrutiny.
    
    Attributes:
    - financial_statements: The financial statements of the company being audited.
    - auditor: The auditor who performed the audit.
    - opinion_type: The type of the audit opinion.
    - basis_for_opinion: The basis for the audit opinion.
    - reporting_format: The reporting format of the audit opinion.
    - effects_of_opinion: The effects of the audit opinion.
    
    Methods:
    - describe_audit_opinion(): Prints the audit opinion type, basis, reporting format, and effects.    
    """
    def __init__(self, financial_statements, auditor,opinion_type, basis_for_opinion, reporting_format, effects_of_opinion):
        super().__init__(financial_statements, auditor)
        self.opinion_type = opinion_type
        self.basis_for_opinion = basis_for_opinion
        self.reporting_format = reporting_format
        self.effects_of_opinion = effects_of_opinion
    
    def describe_audit_opinion(self):
        print("Opinion type: ", self.opinion_type)
        print("Basis for opinion: ", self.basis_for_opinion)
        print("Reporting format: ", self.reporting_format)
        print("Effects of opinion: ", self.effects_of_opinion)
