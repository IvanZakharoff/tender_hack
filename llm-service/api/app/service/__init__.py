from flask import Flask

from api.app.controller import init_routers

def create_app():
    app = Flask(__name__)
    init_routers(app)
    return app
