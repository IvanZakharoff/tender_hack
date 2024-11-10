import json
from flask_restx import Resource
from api.app.dto.check import CheckDto
from flask import request

from werkzeug.datastructures import FileStorage


api = CheckDto.api



def _find_and_handle_rule_6(rules):
    for rule in rules:
        ...


@api.route('/session')
class ExampleCreateApi(Resource):
    @api.doc('create_example')
    # @api.expect(upload_parser)
    @api.response(200, 'Success', CheckDto.session)
    def post(self):
        """Получить заметку по идентификатору"""
        rules = json.loads(request.form['rules'])
        contract = request.files['contract']
        tz = request.files['tz']

        if 'files' not in request.files:
            return {'message': 'No files were uploaded'}
        
        files = request.files.getlist('files')

        data = api.payload

        dto = {
            'clear_contract': clean_text(),
            'clear_tz': clean_tx(),

        }

        print(files, data)

        return data
