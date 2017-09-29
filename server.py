from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

from model import db, connect_to_db
from oauth2client.client import OAuth2WebServerFlow

import os




app = Flask(__name__)


app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined




client_id = os.environ["GGL_ID"]
client_secret = os.environ["GGL_SECRET"]

scope = "https://www.googleapis.com/auth/fitness.activity.read"
flow = OAuth2WebServerFlow(client_id=client_id,
                           client_secret=client_secret,
                           scope=scope,
                           redirect_uri='http://localhost:5000/auth_return/')
                                        
from views import *

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(port=5000, host='0.0.0.0')