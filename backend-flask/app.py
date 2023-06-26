from flask import Flask
from flask import request, g
from flask_cors import cross_origin
import os

from aws_xray_sdk.core import xray_recorder
from lib.cognito_jwt_token import jwt_required

from lib.rollbar import init_rollbar
from lib.xray import init_xray
from lib.honeycomb import init_honeycomb
from lib.cors import init_cors
from lib.cloudwatch import init_cloudwatch
from lib.helpers import model_json

import routes.activities
import routes.users
import routes.messages
import routes.general

app = Flask(__name__)

init_xray(app)
with app.app_context():
    rollbar = init_rollbar(app)
init_honeycomb(app)
init_cors(app)
#  init_cloudwatch(response)    

# load routes -----------
routes.activities.load(app)
routes.users.load(app)
routes.messages.load(app)
routes.general.load(app)

if __name__ == "__main__":
  app.run(debug=True)