from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import Monster, Attack, LevelLookup, User, Goal, GoalStatus, UserStatus
from model import db, connect_to_db
import datetime


app = Flask(__name__)


app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/user/<username>')
def index(username):
	"""Homepage."""
	now = datetime.datetime.now()
	user = User.query.filter(User.username==username).one()

	status = user.userstatus[-1]

	xp = status.current_xp
	hp = status.current_hp
	level = status.level


	goals = [goal for goal in user.goal if goal.valid_from < now and goal.valid_to > now]
	progress = sorted([(status.date_recorded, status.value) for status in goals[-1].goalstatus])[0]


	return render_template("user_page.html", username=username, goals=goals, 
		                   goalstatus = progress, xp=xp, hp=hp, level=level )


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(port=5000, host='0.0.0.0')