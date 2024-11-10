from .analyzer import LLMManager
from .question_manager import QuestionManager
from .llm_answer_manager import LlmAnswerManager
from ..service.semantic_equality import symbolic_levenshtein, semantic_cosine

class SessionManager:
    #TODO somehow insert files
    def __init__(self, request_data):
        clear_contract = request_data["clear_contract"]
        self.llm_manager = LLMManager(clear_contract)
        self.request_args = request_data.get("rules")
        self.questions = {}
        self.llm_answers_to_compare = {}
        self.result_list = []
        
        
    def parse_args(self):
        for rule_dict in self.request_args:
            rule_id = rule_dict.get('rule')
            args = rule_dict.get('args')
            self.questions[rule_id] = QuestionManager(rule_id, args)
            
    def ask_questions(self):
        for rule_id, question in self.questions.items():
            question:QuestionManager = question
            self.llm_answers_to_compare[rule_id] = {}
            self.llm_answers_to_compare[rule_id]['raw_answers'] = self.llm_manager.ask_saiga(question)
            self.llm_answers_to_compare[rule_id]['args_to_compare'] = question.args
            
    def check(self):
        for rule_id, data in self.llm_answers_to_compare.items():
            raw_answers = data['raw_answers']
            args_to_compare = data['args_to_compare']
            
            checker = LlmAnswerManager(rule_id, raw_answers, args_to_compare)
            checker.check()
            rule_res = {
                rule_id,
                checker.status,
                checker.reason
            }
            self.result_list.append(rule_res)
            
        final_result = {
            "results":self.result_list
        }
        
        return final_result