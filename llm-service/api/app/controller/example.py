from flask_restx import Resource
from api.app.dto.example import ExampleDTO


api = ExampleDTO.api

    
@api.route('/example/<int:id_>')
@api.param('id', 'Идентификатор заметки')
class ExampleApi(Resource):
    @api.doc('create_example')
    @api.response(200, 'Success', ExampleDTO.example_scheme)
    def get(self, id_):
        """Получить заметку по идентификатору"""
        if id_==0:
            api.abort(404, "not found")
        return {
            'id': id_, 
            'example': 'example'
        }


@api.route('/example')
class ExampleCreateApi(Resource):
    @api.doc('create_example')
    # @api.expect(ExampleDTO.example_scheme, validate=True)
    @api.response(200, 'Success', ExampleDTO.example_scheme)
    def post(self):
        """Получить заметку по идентификатору"""
        data = api.payload()
        api.abort(400, "bad request")
        return data


