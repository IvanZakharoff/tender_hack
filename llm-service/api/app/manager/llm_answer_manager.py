
from ..service.semantic_equality import semantic_cosine, symbolic_levenshtein


class LlmAnswerManager:
    def __init__(self, rule_id:Literal[1, 2, 3, 4, 5, 6], raw_answers, params):
        self.raw_answers: list = raw_answers
        self.params = params
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
        return questions[int(rule)]

    def check_name_equality(self):
        ks_name = self.args["contractName"]
        llm_answer = self.raw_answers[0]
        
        res = re.split(r':', my_str, 3)
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
        lm_answer = self.raw_answers[0]
        
        res = re.split(r':', my_str, 3)
        llm_certificates_or_no = ((re.sub(r'[^\w\s]', ' ', res[2]).strip()).split(' '))[0]
        list_sert = res[3]

            
    def check_supply_shedule_and_stage(self):
        pass
            
    def check_contract_prize(self):
        pass
            
    def check_technical_specifications(self):
        pass
        
        
        