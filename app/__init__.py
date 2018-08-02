from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS

import config


def create_app(config_name):
    '''Function to create a flask app depending on the configuration passed'''

    app = Flask(__name__)
    api = Api(app)
    CORS(app)
    app.config.from_object(config.app_config[config_name])
    app.url_map.strict_slashes = False

    with app.app_context():
        from app.resources.users import SignupResource, LoginResource
        from app.resources.entries import EntryResource

    api.add_resource(SignupResource, '/api/v1/user/signup')
    api.add_resource(LoginResource, '/api/v1/user/login')
    api.add_resource(EntryResource, '/api/v1/user/entries',
                     '/api/v1/user/entries/<int:entry_id>')

    @app.route("/")
    def index():
        return render_template("docs.html")
    return app
