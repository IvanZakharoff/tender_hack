from flask_restx import Namespace, fields

class ExampleDTO:
    api = Namespace('example', description='example')

    example_scheme = api.model('chat_in', {
        'id': fields.Integer(required=True, description='The user chat channel id'),
        'example': fields.String(required=True, description='The user name'),        
    })


