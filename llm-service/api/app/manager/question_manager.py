from typing import Literal

from api.app.exceptions.question_manager import *

class QuestionManager:
    filter_enum = [
            'NAME_EQUALITY', # одинаковые имена в поле и договоре | семантическая близость    
            'Contract Guarantee', # обеспечение выполгнения контракта | поле всегда есть и либо трнебуем либо нет
            'CERTIFICATION', # наличие серификатов и лицензий | поле есть не всегда, если оно есть то нужно что то нужно проверить совпадение каждого
            'SUPPLY_SCHEDULE_AND_STAGE', # график поставки и этап поставки | Всегда есть, сверяем с ллм оба    и то и то!!
            'CONTRACT_PRICE', # максимальная и начальная цена контракта | Если есть поля цены, то сверяем и то и то, мб тоьлко одно из полей, если есть, прооверяем
            'TECHNICAL_SPECIFICATION', # ТЗ | Если есть файл ТЗ то наименование тз должно совпасть (если есть) значение характеристик спецификации в тз, количество товаров и услуг должно совпадать, если в тз характеристик больше то норм, живем, иначе пизда
        ]
    
    def __init__(self, rule:Literal[1, 2, 3, 4, 5, 6], args:dict):
        self.args = args
        self.ask = self._find_out_rule(rule)
        
    def _find_out_rule(self, rule):
        questions = [
            self.ask_name_equality,
            self.ask_contract_guarantee,
            self.ask_certification,
            self.ask_supply_shedule_and_stage,
            self.ask_contract_prize,
            self.ask_technical_specifications
        ] 
        return questions[int(rule)]
    
    def ask_name_equality(self):
        
        if expected_session_name := self.args['contractName']:
            if type(expected_session_name) == str:
                raise AskNameEqualityArgsException('Name should be string')
        #TODO
        question_text = 'Верни наименование закупки. Если наименования нет, напиши, что наименования нет'
        
    def ask_contract_guarantee(self):
        if not isinstance(self.args, dict) or len(self.args) != 1:
            raise AskContractGuaranteeArgsException("Invalid arguments structure")

        if 'isContractGuaranteeRequired' not in self.args:
            raise AskContractGuaranteeArgsException("Missing 'isContractGuaranteeRequired' key")

        if not isinstance(self.args['isContractGuaranteeRequired'], bool):
            raise AskContractGuaranteeArgsException("'isContractGuaranteeRequired' must be a boolean")
        
        contract_required = self.args['isContractGuaranteeRequired']
        #TODO
        question_text = 'Скажи,требуется ли обеспечение исполнения контракта, и ответь да или нет на вопрос требуется ли обеспечение исполнения контракта'
        
    def ask_certification(self):
        if not isinstance(self.args, dict) or len(self.args) != 1:
            raise AskCertificationArgsException("Invalid arguments structure")

        if 'licenseFiles' not in self.args:
            raise AskCertificationArgsException("Missing 'licenseFiles' key")

        license_files = self.args['licenseFiles']

        if license_files is None:
            # No licenses needed
            pass

        if not isinstance(license_files, (list, tuple)):
            raise AskCertificationArgsException("'licenseFiles' must be a list or None")


        #TODO
        question_text = ''
        
    def ask_supply_shedule_and_stage(self):
        if not isinstance(self.args, dict) or len(self.args) != 3:
            raise AskSupplySheduleAndStageArgsException("Invalid arguments structure")

        required_fields = ['periodDaysFrom', 'periodDaysTo', 'deliveryStage']
        
        for field in required_fields:
            if field not in self.args:
                raise AskSupplySheduleAndStageArgsException(f"Missing '{field}' key")
            
            if not isinstance(self.args[field], str):
                raise AskSupplySheduleAndStageArgsException(f"'{field}' must be a string")

        
        period_days_from = self.args['periodDaysFrom']
        period_days_to   = self.args['periodDaysTo']
        delivery_stage   = self.args['deliveryStage']
        
        #TODO
        question_text = ''
    
    def ask_contract_prize(self):
        
        if not isinstance(self.args, dict) or len(self.args) != 2:
            raise AskContractPrizeArgsException("Invalid arguments structure")

        required_fields = ['startCost', 'maxContractCost']
        
        for field in required_fields:
            if field not in self.args:
                raise AskContractPrizeArgsException(f"Missing '{field}' key")
            
            if not isinstance(self.args[field], str):
                raise AskContractPrizeArgsException(f"'{field}' must be a string")

        
        start_cost = self.args['startCost']
        max_contract_cost = self.args['maxContractCost']
        #TODO
        question_text = ''
    
    def ask_technical_specifications(self):
        
        
        items:list = self.args
        if not isinstance(self.args, dict) or 'items' not in self.args:
            raise AskaskTechnicalSpecificationsArgsException("Invalid arguments structure")

        if not isinstance(self.args['items'], list):
            raise AskaskTechnicalSpecificationsArgsException("Items should be a list")

        for item in self.args['items']:
            if not isinstance(item, dict):
                raise AskaskTechnicalSpecificationsArgsException("Each item should be a dictionary")
            
            required_keys = ['name', 'properties', 'quantity']
            if not all(key in item for key in required_keys):
                raise AskaskTechnicalSpecificationsArgsException("Missing required keys in item")

            if not isinstance(item['properties'], list):
                raise AskaskTechnicalSpecificationsArgsException("Properties should be a list")

            for prop in item['properties']:
                if not isinstance(prop, dict):
                    raise AskaskTechnicalSpecificationsArgsException("Each property should be a dictionary")
                
                required_keys = ['name', 'value']  # Added 'measurement' to the required keys
                if not all(key in prop for key in required_keys):
                    raise AskaskTechnicalSpecificationsArgsException("Missing required keys in property")

        
 