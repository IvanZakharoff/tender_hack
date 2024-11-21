from flask_restx import Namespace, fields
from .enums import RuleEnum

class CheckDto:
    api = Namespace('check')


    rule = api.model('rule', {
        'rule': fields.Integer(enum=[status.value for status in RuleEnum], required=True, description='Status of the item'),
        'args': fields.Raw(description='A dictionary of attributes')
    })

    session = api.model('session', {
        'text': fields.String(required=True, description='The all text'),    
        'rules': fields.List(fields.Nested(rule))  
    })

