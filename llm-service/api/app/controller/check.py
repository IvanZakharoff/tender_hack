from flask_restx import Resource
from api.app.dto.check import CheckDto

api = CheckDto.api


@api.route('/session')
class ExampleCreateApi(Resource):
    @api.doc('create_example')
    @api.expect(CheckDto.session, validate=True)
    @api.response(200, 'Success', CheckDto.session)
    def post(self):
        """Получить заметку по идентификатору"""
        data = api.payload

        return data
