from .analyzer import LLMManager
from .question_manager import QuestionManager
from ..service.semantic_equality import symbolic_levenshtein, semantic_cosine

class SessionManager:
    def __init__(self, request_data):
        clear_contract = request_data["clear_contract"]
        self.llm_manager = LLMManager(clear_contract)
        self.request_args = request_data.get("rules")
        self.questions = {}
        self.llm_answers_to_compare = {}
        
        
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
            
    def blya_pizda_what_am_i_doing_omg_semantic_ass(self):
        print()
        pass