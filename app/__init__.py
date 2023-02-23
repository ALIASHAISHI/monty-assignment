from flask import Flask, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from api.views import api
import os

def create_app():
    app = Flask(__name__)
    
    app.config['host'] = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    app.config['port'] = os.getenv('FLASK_RUN_PORT', '0.0.0.0')
    
    app.register_blueprint(api)
    
    @app.route("/spec")
    def spec():
        return jsonify(swagger(app))
    
    SWAGGER_URL = ''  # URL for exposing Swagger UI (without trailing '/')
    API_URL = '/spec'  # Our API url (can of course be a local resource)

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={ 
            'app_name': "Ali Ashaishi Assignment"
        }
    )

    app.register_blueprint(swaggerui_blueprint)
    
    return app