from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class BaseRule:
    rule: str
    text: str
    args: dict

@dataclass
class ParsedArgsRule(BaseRule):
    parsed_args: dict

@dataclass
class RuleWrapper:
    rules: List[BaseRule]

@dataclass
class NameEqualityRule(ParsedArgsRule):
    contractName: str

@dataclass
class ContractEnforcementRule(BaseRule):
    isContractGuaranteeRequired: bool

@dataclass
class CertificationRule(BaseRule):
    licenseFiles: Optional[List[str]] = None

@dataclass
class SupplyScheduleAndStageRule(BaseRule):
    periodDaysFrom: str
    periodDaysTo: str
    deliveryStage: str

@dataclass
class ContractCostRule(BaseRule):
    startCost: str
    maxContractCost: str

@dataclass
class TechnicalSpecificationRule(BaseRule):
    items: List[dict]


@dataclass
class RulesDTO(RuleWrapper):
    def __post_init__(self):
        # Ensure uniqueness of "rule" fields
        seen_rules = set()
        for rule in self.rules:
            if rule.rule in seen_rules:
                raise ValueError(f"Duplicate rule found: {rule.rule}")
            seen_rules.add(rule.rule)

# Example usage
rules_data = RulesDTO(
    rules=[
        NameEqualityRule(rule="NAME_EQUALITY", text="<contract_text>", parsed_args={"contractName": "name"}),
        ContractEnforcementRule(rule="CONTRACT_ENFORCEMENT", text="<text>", isContractGuaranteeRequired=True),
        CertificationRule(rule="CERTIFICATION", text="<text>", licenseFiles=None),
        SupplyScheduleAndStageRule(rule="SUPPLY_SCHEDULE AND STAGE", text="<text>", 
                                  periodDaysFrom="<text>", periodDaysTo="<text>", deliveryStage="smth text"),
        ContractCostRule(rule="CONTRACT_COST", text="<text>", startCost="<text>", maxContractCost="<text>"),
        TechnicalSpecificationRule(rule="TECHNICAL_SPECIFICATION", text="<text ts>", items=[{
            "name": "<text>",
            "properties": [{"name": "<text>", "value": "<text>", "measurement": "<text>"},],
            "quantity": "<text>",
            "totalCost": "<text>"
        }])
    ]
)
