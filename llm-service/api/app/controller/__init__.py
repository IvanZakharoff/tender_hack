from flask import Blueprint
from flask_restx import Api

from . import example
from . import check



def init_routers(app):
    blueprint = Blueprint('api', __name__, url_prefix='')
    api = Api(blueprint, 
              title=f'Ml service API',
              description=f'API for ML service',
              doc='/swagger')
    
    api.add_namespace(example.api)
    api.add_namespace(check.api)

    app.register_blueprint(blueprint)

