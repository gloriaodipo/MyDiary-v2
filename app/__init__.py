from flask import Flask

import config

def create_app(config_name):
    '''Method to create a flask app depending on the configuration passed'''

    app = Flask(__name__)

    app.config.from_object(config.app_config[config_name])
    
    return app