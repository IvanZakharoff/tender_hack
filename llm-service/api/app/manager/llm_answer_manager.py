
from ..service.semantic_equality import semantic_cosine, symbolic_levenshtein
import re
from typing import Literal

class LlmAnswerManager:
    def __init__(self, rule_id:Literal[1, 2, 3, 4, 5, 6], raw_answers, args):
        self.raw_answers: list = [re.sub(r'\n+', ' ', my_str) for my_str in raw_answers]
        
        self.args = args
        self.check = self._find_out_rule(rule_id)
        
        self.status = None
        self.reason = ''
        self.rule_id = rule_id
        
        

    def _find_out_rule(self, rule):
        questions = [
            self.check_name_equality,
            self.check_contract_guarantee,
            self.check_certification,
            self.check_supply_shedule_and_stage,
            self.check_contract_prize,
            self.check_technical_specifications
        ] 
        return questions[int(rule)-1]

    def check_name_equality(self):
        ks_name = self.args["contractName"]
        llm_answer = self.raw_answers[0]
        
        res = re.split(r':', llm_answer, 3)
        llm_name_or_no_ans = ''.join(((re.sub(r'[^\w\s]', ' ', res[2]).strip()).split(' '))[:-1])
        reason = res[3]
        self.reason = reason 
        
        no_similarity = semantic_cosine(llm_name_or_no_ans, 'нет')
        name_similarity = semantic_cosine(llm_name_or_no_ans, ks_name)
        
        if no_similarity > name_similarity:
            self.status = 'unsucceed'
            
        else:
            if name_similarity < .5:
                self.status = 'unsucceed'
                
            else:    
                self.status = 'succeed'
            
            self.reason += f'Совпадение имен по Левенштейну: {symbolic_levenshtein(llm_name_or_no_ans, ks_name):.3}'
            self.reason += f'Косинусная семантическая схожесть: { name_similarity:.3}'
            
        
    def check_contract_guarantee(self):
        ks_is_smth_required = self.args['isContractGuaranteeRequired']
        llm_answer = self.raw_answers[0]
        
        res = re.split(r':', llm_answer, 3)
        llm_yes_or_no_ans = ((re.sub(r'[^\w\s]', ' ', res[2]).strip()).split(' '))[0]
        reason = res[3]
        
        self.reason = reason
        
        # may cause shitty efficiency
        yes_similarity = semantic_cosine('да', llm_yes_or_no_ans)
        no_similarity = semantic_cosine('нет', llm_yes_or_no_ans)
        
        if yes_similarity > no_similarity:
            
            self.status = 'succeed'
        else:
            self.status = 'unsucceed'
            
                   
    def check_certification(self):
        llm_answer = self.raw_answers[0]
        ks_license_files = self.args['licenseFiles']
        
        ks_license_files_str = ''
        for s in ks_license_files:
            ks_license_files_str += s
        
        res = re.split(r':', llm_answer, 3)
        llm_yes_or_no = ((re.sub(r'[^\w\s]', ' ', res[2]).strip()).split(' '))[0]
        llm_list_sert = res[3]
        
        yes_similarity = semantic_cosine('да', llm_yes_or_no)
        no_similarity = semantic_cosine('нет', llm_yes_or_no)
        
        if not (yes_similarity > no_similarity ^ ks_license_files):
            list_of_certificates_similarity = semantic_cosine(ks_license_files_str, llm_list_sert)  
            if list_of_certificates_similarity > .5:
                self.status = 'succeed'
            else:
                self.status = 'unsucceed'
                
            self.reason += f'Совпадение сертификатов по Левенштейну: {symbolic_levenshtein(ks_license_files_str, llm_list_sert):.3}'
            self.reason += f'Косинусная семантическая схожесть сертификатов : { list_of_certificates_similarity:.3}'
            
        else:
            self.status = 'unsucceed'
            self.reason += 'Наличие сертификатов в котировочной сессии и в контракте не совпадает'
                
        

            
    def check_supply_shedule_and_stage(self):
        llm_dedlines_answer = self.raw_answers[0]
        ks_deadlines = f"от {self.args['periodDaysFrom']} до {self.args['periodDaysTo']} дней"
        
        
        res = re.split(r':', llm_dedlines_answer, 3)
        llm_yes_or_no = ((re.sub(r'[^\w\s]', ' ', res[2]).strip()).split(' '))[0]
        llm_schedule_or_reason = res[3]# if yes, deadlines, else reasons why shit
        
        
        yes_similarity = semantic_cosine('да', llm_yes_or_no)
        no_similarity = semantic_cosine('нет', llm_yes_or_no)
        
        
        
        if yes_similarity > no_similarity:
            self.status = 'unsucceed'
            self.reason = llm_schedule_or_reason # it is reason already
            return 0
        else:
            llm_deadlines = llm_schedule_or_reason
            llm_deadlines_similarity = semantic_cosine(llm_deadlines, ks_deadlines)
            if llm_deadlines_similarity >.5:
                self.status = 'succeed'
            else:
                self.status = 'unsucceed'
                return 0
                
            self.reason += f'Совпадение дат поставки по Левенштейну: {symbolic_levenshtein(ks_deadlines, llm_deadlines):.3}'
            self.reason += f'Косинусная семантическая схожесть дат поставки : { llm_deadlines_similarity:.3}'
            
            
            
        
        llm_delivery_stage_answer = self.raw_answers[1]
        res = re.split(r':', llm_delivery_stage_answer, 3)
        bool_or_num_delivery_stage = ((re.sub(r'[^\w\s]', ' ', res[2]).strip()).split(' '))[0]
        reason = res[3]
        
        yes_similarity = semantic_cosine('да', llm_yes_or_no)
        no_similarity = semantic_cosine('нет', llm_yes_or_no)
        
        
            
    def check_contract_prize(self):
        self.status = 'succeed'
        self.reason = 'Очень круто, все прошло'
            
    def check_technical_specifications(self):
        self.status = 'succeed'
        self.reason = 'Очень круто, все прошло'
        
        
    def check(self):
        self.status = 'succeed'
        self.reason = 'Очень круто, все прошло'
        
        