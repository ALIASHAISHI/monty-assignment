from flask import Flask
from api.views import api
import os

def create_app():
    app = Flask(__name__)
    
    app.config['host'] = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    app.config['port'] = os.getenv('FLASK_RUN_PORT', '0.0.0.0')
    
    app.register_blueprint(api)
    
    return app