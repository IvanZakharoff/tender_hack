from email import utils
import io
import json
from PyPDF2 import PdfReader
from flask_restx import Resource
from api.app.dto.check import CheckDto
from flask import request
import fitz
from docx import Document


api = CheckDto.api

def extract_text_from_pdf(pdf_bytes):
    # Создаем объект BytesIO из байтов PDF файла
    pdf_stream = io.BytesIO(pdf_bytes)
    
    # Открываем PDF файл
    reader = PdfReader(pdf_stream)
    
    # Извлекаем текст из каждой страницы
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    return text.strip()


def extract_text_from_docx(docx_bytes):
    # Создаём объект BytesIO из байтов DOCX файла
    docx_stream = io.BytesIO(docx_bytes)
    
    # Открываем документ
    document = Document(docx_stream)
    
    # Извлекаем текст из каждого параграфа
    text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    
    return text.strip()


def _find_and_handle_rule_6(rules, tz):
    for rule in rules:
        if rule['rule'] == 6: 
            rule['text'] = get_text(tz)
            return 

def get_text(filestorage):
    if filestorage.filename.endswith('.docx'):
        return extract_text_from_docx(docx_bytes=filestorage.read())
    elif filestorage.filename.endswith('.pdf'):
        return extract_text_from_docx(docx_bytes=filestorage.read())
    else:
        return ''



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

        print(contract.filename)

        text = get_text(contract)
    
        rules = _find_and_handle_rule_6(tz)

        dto = {
            'clear_contract': utils.convert_pdf_to_text(),
        }


        # fitz.open(stream=input_bytes, filetype="pdf")
        all_text = ""
        # for page in fitz.pages():
        #     all_text += page.get_text("text")

        return {
        
        }
