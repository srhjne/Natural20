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
import random

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

@app.route('/')
def landing_page():
	if session.get("user_id"):
		user = User.query.get(session["user_id"])
		return redirect("/user/%s"%user.username)
	else:
		return redirect("/login")

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
		if hp == 0:
			return render_template("dead.html")
		else:
			level = status.level

			progresses = []
			goals = [goal for goal in user.goal if goal.valid_from < now and goal.valid_to > now]
			for goal in goals:
				progress = sorted([(status.date_recorded, status.value, (status.value/goal.value)*100, goal) for status in goal.goalstatus])[-1]
				progresses.append(progress)


			return render_template("user_page.html", username=username,  
				                   goalstatus = progresses, xp=xp, hp=hp, level=level)


@app.route('/registration')
def registration():
	return render_template("registration.html")


@app.route('/registration', methods=["POST"])
def registration_handle():
	username = request.form.get("username")
	if User.query.filter(User.username==username).all() or not username or " " in username:
		flash("Sorry that username is already taken!")
		return redirect("/registration")
	else:
		password = request.form.get("password")
		confirm_password = request.form.get("confirm_password")
		if confirm_password != password or not password:
			flash("Passwords do not match")
			return redirect("/registration")
		else:
			email = request.form.get("email")
			if email and " " not in email and "@" in email:
				user = User(username=username, email=email, password=password)
				db.session.add(user)
				db.session.commit()
				user_db = User.query.filter(User.username==username).first()
				userstatus = UserStatus(user_id=user_db.user_id,current_hp=12,current_xp=0,
										level=1,date_recorded=datetime.datetime.now())
				db.session.add(userstatus)
				db.session.commit()
				flash("Thanks for registering!")
				return redirect("/login")
			else:
				flash("Please enter a valid email address")
				return redirect("/registration")


@app.route("/reroll", methods=["POST"])
def reroll():
	user_id = session.get("user_id")
	if not user_id:
		flash("You must be logged in to view this")
		return redirect("/login")
	else:
		user = User.query.get(user_id)
		userstatus = UserStatus(user_id=user_id, current_xp=0, current_hp=12, level=1, date_recorded=datetime.datetime.now())
		db.session.add(userstatus)
		db.session.commit()
		return redirect("/user/%s"%user.username)



@app.route('/login')
def login():
	return render_template("login.html")



@app.route('/auth_return/', methods=["GET"])
def auth_ret():
	code = request.args.get("code")
	credentials = flow.step2_exchange(code)
	http = httplib2.Http()
	http = credentials.authorize(http)
	global service 
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


@app.route('/outcome.json')
def outcome_json():
	user = User.query.get(int(session.get("user_id")))
	userstatuses = user.userstatus
	most_recent_status = userstatuses[-1] # this works because I applied ordering in model.py
	goal_list = []

	new_xp = most_recent_status.current_xp
	new_hp = most_recent_status.current_hp

	goals = [goal for goal in user.goal if goal.valid_to < datetime.datetime.now() and not goal.resolved]
	for goal in goals:
		goalstatus_max = max([goalstatus.value for goalstatus in goal.goalstatus])
		if goalstatus_max >= goal.value:
			# good things happen
			goal_list.append({"username": user.username,"achieved": True, "goal_type": goal.goal_type, "goal_value" : goal.value,
						      "valid_from": goal.valid_from, "valid_to" : goal.valid_to,
						      "goal_id": goal.goal_id, "xp": goal.xp, "current_xp": most_recent_status.current_xp,
						      "current_level": most_recent_status.level})
			
			new_xp += goal.xp
			
			goal.resolved = "Y"
		else:
			# bad things happen
			mincr = most_recent_status.levellookup.min_cr
			maxcr = most_recent_status.levellookup.max_cr
			monster_list = Monster.query.filter(Monster.cr <= maxcr, Monster.cr >= mincr).all()
			monster = random.choice(monster_list)
			attack = random.choice(monster.attack)
			if attack.num_dice:
				damage_val = attack.num_dice*random.randint(1,attack.type_dice)
				if attack.dice_modifier:
					damage_val += attack.dice_modifier
			else:
				damage_val = avg_damage
			goal_list.append({"username": user.username ,"achieved": False, "goal_type": goal.goal_type, "goal_value" : goal.value,
						      "valid_from": goal.valid_from, "valid_to" : goal.valid_to,
						      "goal_id": goal.goal_id, "xp": goal.xp, "current_xp": most_recent_status.current_xp,
						      "current_level": most_recent_status.level, "monster": monster.name   ,
						      "attack":{"name": attack.name,
						                "damage_type": attack.damage_type,
						                "damage_val": damage_val
						                }})	
			new_hp -= damage_val

			goal.resolved = "Y"
	level = LevelLookup.query.filter(LevelLookup.required_xp <= new_xp).order_by(LevelLookup.level).all()
	print level
	new_level=level[-1]
	if new_level.level > most_recent_status.level:
		new_hp = new_level.hit_point_max
	else:
		new_hp = max(0, new_hp)


	new_status = UserStatus(user_id=user.user_id, current_xp = new_xp, current_hp=new_hp, level=new_level.level, 
							date_recorded=datetime.datetime.now())	
	db.session.add(new_status)
	db.session.commit()
	return jsonify(goal_list)



@app.route('/outcome')
def outcome():
	return render_template("outcome.html")


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

	users = User.query.filter(User.username == username).all()
	if users:
		user = users[0]
		if user.password == password:
			session["user_id"] = user.user_id
			auth_uri = flow.step1_get_authorize_url()
			return redirect(auth_uri)
			# return redirect("/user/%s"%username)
		else:
			flash("Incorrect Password")
			return redirect("/login")
	else:
		flash("Incorrect username")
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