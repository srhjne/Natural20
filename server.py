from flask import Flask
from flask import jsonify, render_template, redirect, request, flash, session, g

from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

from model import db, connect_to_db
from oauth2client.client import OAuth2WebServerFlow

import os
import datetime




app = Flask(__name__)


app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined




client_id = os.environ["GGL_ID"]
client_secret = os.environ["GGL_SECRET"]

scope = "https://www.googleapis.com/auth/fitness.activity.read"
flow = OAuth2WebServerFlow(client_id=client_id,
                           client_secret=client_secret,
                           scope=scope,
                           redirect_uri='http://natural20.sarahjaneiom.com/auth_return/')

global JS_TESTING_MODE
JS_TESTING_MODE = False

# @app.before_request
# def check_login_time():
#   if request.path not in ('/login', '/logout', '/registration', '/clock.json'):
#     if session.get("login_time", None) and session.get("user_id", None):
#       if (datetime.datetime.now() - session.get("login_time")).total_seconds() > 60*60:
#         flash("Your session has timed out, please log in again")
#         del session["user_id"]
#         return redirect("/login")
#     else:
#       flash("Please log in to view this")
#       return redirect("/login")
#   g.jasmine_tests = False
  

                                        
from views import *

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)


    # import sys
    # if sys.argv[-1] == "jstest":
    #     global JS_TESTING_MODE
    #     JS_TESTING_MODE = True
    # else:
    #     JS_TESTING_MODE = False
    # print JS_TESTING_MODE


    app.run(port=5000, host='0.0.0.0')
