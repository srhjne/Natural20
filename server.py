from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import Monster, Attack, LevelLookup, User, Goal, GoalStatus, UserStatus
from model import db, connect_to_db
from oauth2client.client import OAuth2WebServerFlow
import httplib2
from apiclient.discovery import build
import os
import datetime

import fitness_helper_functions as fhf


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


@app.route('/user/<username>')
def profile_page(username):
	"""profile page"""

	user = User.query.filter(User.username==username).one()
	print "user id", session.get("user_id")
	if session.get("user_id", "") != user.user_id:
		flash("You must be logged in to view this page")
		return redirect("/login") 
	else:
		now = datetime.datetime.now()
		

		status = user.userstatus[-1]

		xp = status.current_xp
		hp = status.current_hp
		level = status.level

		progresses = []
		goals = [goal for goal in user.goal if goal.valid_from < now and goal.valid_to > now]
		for goal in goals:
			progress = sorted([(status.date_recorded, status.value, goal) for status in goal.goalstatus])[-1]
			progresses.append(progress)


		return render_template("user_page.html", username=username,  
			                   goalstatus = progresses, xp=xp, hp=hp, level=level)


@app.route('/login')
def login():
	return render_template("login.html")



@app.route('/auth_return/', methods=["GET"])
def auth_ret():
	code = request.args.get("code")
	credentials = flow.step2_exchange(code)
	http = httplib2.Http()
	http = credentials.authorize(http)
	service = build('fitness', 'v1', http=http)

	if session.get("user_id"):
		goals_to_resolve=[]
		user = User.query.get(int(session.get("user_id")))
		goals = [goal for goal in user.goal if goal.valid_from < datetime.datetime.now() and not goal.resolved]
		for goal in goals:
			if goal.goal_type == "Steps":
				millisstart = fhf.get_millis_date(goal.valid_from)
				millisend = fhf.get_millis_date(goal.valid_to)
				delta = millisend - millisstart
				agg = service.users().dataset().aggregate(userId="me",
				body={"aggregateBy":[{
			    	"dataTypeName": "com.google.step_count.delta",
			    	"dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
			  		}],
			  		"bucketByTime": { "durationMillis": delta }, # This is 24 hours
			  		"startTimeMillis": millisstart, #start time
			  		"endTimeMillis": millisend # End Time
			  		})


			
				if len(agg.execute()['bucket'][0]['dataset'][0]['point']) == 0:
					return "No data"
				else:
					print "Hooray you have done %s Steps" % agg.execute()['bucket'][0]['dataset'][0]['point'][0]['value'][0]['intVal']
					value = agg.execute()['bucket'][0]['dataset'][0]['point'][0]['value'][0]['intVal']
					goalprogress = GoalStatus(goal_id = goal.goal_id, date_recorded = datetime.datetime.now(), value=value)
					db.session.add(goalprogress)
					db.session.commit()
				if datetime.datetime.now() > goal.valid_to and goal.resolved is None:
					goals_to_resolve.append(goal)
		print goals_to_resolve
		if goals_to_resolve:
			return redirect("/outcome")
		else:			
			return redirect("/user/%s" % user.username)
	else:
		flash("You need to log in")
		return redirect("/login")


@app.route('/outcome')
def outcome():
	return "monster page will go here"


@app.route('/test')
def test():
	auth_uri = flow.step1_get_authorize_url()
	return redirect(auth_uri)


@app.route('/set_goal', methods=['GET'])
def set_goals():
	if not session.get('user_id'):
		flash("You must be logged in to view this")
		return redirect("/login")
	else:
		return render_template("set_goals.html")



@app.route("/calc_xp.json", methods=['GET'])
def calc_xp():
	user = User.query.get(session.get('user_id'))
	goal_type = request.args.get("goal_type")
	goal_value = request.args.get("value")
	goal_value = int(goal_value)
	valid_from_u = request.args.get("valid_from")
	valid_from = datetime.datetime.strptime(valid_from_u, "%Y-%m-%d")
	valid_to_u = request.args.get("valid_to")
	valid_to = datetime.datetime.strptime(valid_to_u, "%Y-%m-%d")
	value = request.args.get("value")
	print "Position 2"
	timedelta = (valid_to - valid_from).total_seconds()
	scaled_value_test = goal_value/timedelta

	max_xp = 500

	goals = Goal.query.filter(Goal.goal_type == goal_type, Goal.user_id==user.user_id).all()
	if not goals:
		print "Position 3"
		return jsonify({"xp": 500})
	else:
		print "Position 4"
		for goal in goals:
			timedelta = (goal.valid_to - goal.valid_from).total_seconds()
			scaled_value = goal.value/timedelta
			ratio = scaled_value_test/scaled_value
			if ratio < 0.8:
				print "Position 5"
				return jsonify({"xp": 200})
			elif ratio >= 0.8 and ratio < 1.1:
				max_xp = 300
		print "Position 6", max_xp
		return jsonify({"xp":max_xp})






@app.route('/set_goal', methods=['POST'])
def set_goal_db():
	if not session.get('user_id'):
		flash("You must be logged in to view this")
		return redirect("/login")
	else:
		user = User.query.get(session.get('user_id'))
		goal_type = request.form.get("goal_type")
		goal_value = request.form.get("value")
		goal_value = int(goal_value)
		valid_from_u = request.form.get("valid_from")
		valid_from = datetime.datetime.strptime(valid_from_u, "%Y-%m-%d")
		valid_to_u = request.form.get("valid_to")
		valid_to = datetime.datetime.strptime(valid_to_u, "%Y-%m-%d")
		
		timedelta = (valid_to - valid_from).total_seconds()
		scaled_value_test = goal_value/timedelta

		xp = 500

		goals = Goal.query.filter(Goal.goal_type == goal_type, Goal.user_id==user.user_id).all()
		if not goals:
			xp = 500
		else:
			for goal in goals:
				timedelta = (goal.valid_to - goal.valid_from).total_seconds()
				scaled_value = goal.value/timedelta
				ratio = scaled_value_test/scaled_value
				if ratio < 0.8:
					xp = 200
					break
				elif ratio >= 0.8 and ratio < 1.1:
					xp = 300
			
		goal = Goal(user_id=user.user_id, xp=xp, goal_type=goal_type, value=goal_value, valid_from=valid_from, valid_to=valid_to )
		db.session.add(goal)
		db.session.commit()
		goal_db = Goal.query.filter(Goal.user_id==user.user_id, Goal.xp==xp, Goal.goal_type==goal_type, Goal.value==goal_value, Goal.valid_from==valid_from, Goal.valid_to==valid_to).first()
		goalstatus = GoalStatus(goal_id=goal_db.goal_id,value=0,date_recorded=valid_from)
		db.session.add(goalstatus)
		db.session.commit()
		auth_uri = flow.step1_get_authorize_url()
		return redirect(auth_uri)
		





@app.route('/login', methods=["POST"])
def login_post():
	username = request.form.get("username")
	password = request.form.get("password")

	user = User.query.filter(User.username == username).one()
	if user.password == password:
		session["user_id"] = user.user_id
		auth_uri = flow.step1_get_authorize_url()
		return redirect(auth_uri)
		# return redirect("/user/%s"%username)
	else:
		flash("Incorrect Password")
		return redirect("/login")


@app.route('/logout')
def logout():
	del session["user_id"]
	flash("You are now logged out")
	return redirect("/login")





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(port=5000, host='0.0.0.0')