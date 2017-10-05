from server import app, flow
# from oauth2client.client import OAuth2WebServerFlow
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage

from flask import jsonify, render_template, redirect, request, flash, session

from model import User, Goal, GoalStatus, UserStatus, Monster, Attack, LevelLookup, SleepStatus

import os
import datetime
import random

import fitness_helper_functions as fhf
import dnd_helper_functions as dhf

@app.before_request
def check_login_time():
	if request.path not in ('/login', '/logout', '/registration'):
		if session.get("login_time", None) and session.get("user_id", None):
			if (datetime.datetime.now() - session.get("login_time")).total_seconds() > 60*60:
				flash("Your session has timed out, please log in again")
				del session["user_id"]
				return redirect("/login")
		else:
			flash("Please log in to view this")
			return redirect("/login")

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

	try:
		user = User.query.filter(User.username==username).one()
	except Exception:
		flash("This page does not exist")
		return redirect("/login")
	print "user id", session.get("user_id")
	if session.get("user_id", "") != user.user_id:
		flash("You must be logged in as %s to view this page"% username)
		return redirect("/login") 
	else:
		now = datetime.datetime.now()
		status = user.get_current_status()

		xp = status.current_xp
		hp = status.current_hp
		if hp == 0:
			return render_template("dead.html")
		else:
			level = status.level

			progresses = []
			goals = user.get_current_goals()
			for goal in goals:
				if goal.frequency == "Daily":
					mean_value = goal.get_mean_value_daily()
					progress = goal.get_current_status()
					if goal.goal_type == "Sleep":
						progresses.append([progress.date_recorded.strftime("%I:%M%p %B %d, %Y"), round(mean_value/(60.0*60),2), 100.0*progress.value/goal.value, goal])
					else:
						progresses.append([progress.date_recorded.strftime("%I:%M%p %B %d, %Y"), round(mean_value,2), 100.0*progress.value/goal.value, goal])
				else:
					progress = goal.get_current_status()
					if goal.goal_type == "Sleep":
						progresses.append([progress.date_recorded.strftime("%I:%M%p %B %d, %Y"), progress.value/(60.0*60), 100.0*progress.value/goal.value, goal])
					else:
						progresses.append([progress.date_recorded.strftime("%I:%M%p %B %d, %Y"), progress.value, 100.0*progress.value/goal.value, goal])


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
				User.make_new_user(username=username, email=email, password=password)
				flash("Thanks for registering!")
				return redirect("/login")
			else:
				flash("Please enter a valid email address")
				return redirect("/registration")


@app.route("/reroll", methods=["POST"])
def reroll():
	user_id = session.get("user_id")
	user = User.query.get(user_id)
	user.reroll_stats()
	return redirect("/user/%s"%user.username)



@app.route('/login')
def login():
	return render_template("login.html")



@app.route('/auth_return/', methods=["GET"])
def auth_ret():
	code = request.args.get("code")
	credentials = flow.step2_exchange(code)
	storage = Storage('credentials%s.dat' % (session.get("user_id")))
	storage.put(credentials)

	http = httplib2.Http()
	http = credentials.authorize(http)
	service = build('fitness', 'v1', http=http)

	if session.get("user_id"):
		user = User.query.get(int(session.get("user_id")))
		
		fhf.update_goal_status(user, service)
		if user.get_unresolved_overdue_goals():
			print "Unresolved goals", user.get_unresolved_overdue_goals()
			return redirect("/outcome")
		else:			
			return redirect("/user/%s" % user.username)
	else:
		flash("You need to log in")
		return redirect("/login")


@app.route('/outcome.json')
def outcome_json():
	user = User.query.get(int(session.get("user_id")))
	goal_list = dhf.get_outcome_dict(user)
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
	print "Goal type", goal_type
	goal_value = request.args.get("value")
	print "Goal value", goal_value
	goal_value = int(goal_value)
	valid_from_u = request.args.get("valid_from")
	valid_from = datetime.datetime.strptime(valid_from_u, "%Y-%m-%d")
	valid_to_u = request.args.get("valid_to")
	valid_to = datetime.datetime.strptime(valid_to_u, "%Y-%m-%d")
	frequency = request.args.get("frequency")
	
	xp = user.calc_xp(goal_value, valid_from, valid_to, goal_type, frequency)

	return jsonify({"xp":xp})






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
		frequency = request.form.get("frequency")
		
		xp = user.calc_xp(goal_value, valid_from, valid_to, goal_type, frequency)

		if goal_type == "Sleep":
			goal_value = goal_value*60*60
			
		goal = Goal(user_id=user.user_id, xp=xp, goal_type=goal_type, value=goal_value, valid_from=valid_from, valid_to=valid_to, frequency=frequency )
		goal.commit_goal()
		if goal_type != "Sleep":
			GoalStatus.make_first_status(goal_type, valid_from, valid_to, goal_value, xp, user.user_id)
		else:
			SleepStatus.make_first_sleep_status(valid_from, valid_to, goal_value, xp, user.user_id, frequency)
		if goal_type in ("Steps", "Calories"):
			auth_uri = flow.step1_get_authorize_url()
			return redirect(auth_uri)
		elif goal_type in ("Sleep"):
			return redirect("user/%s"%user.username)
		

@app.route('/login', methods=["POST"])
def login_post():
	username = request.form.get("username")
	password = request.form.get("password")

	users = User.query.filter(User.username == username).all()
	if users:
		user = users[0]
		if user.password == password:
			session["user_id"] = user.user_id
			session["login_time"] = datetime.datetime.now()
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


@app.route("/goal_graph.json")
def goal_graph():
	if session.get("user_id"):
		user = User.query.get(session["user_id"])
		goals = user.get_current_goals()
		goal_dict = {}
		for goal in goals:
			if goal.frequency == "Daily":
				series = goal.get_daily_status_series()
				print series
			else:
				series = goal.get_status_series()
				print series
			goal_dict[goal.goal_id] = {"series": series, "valid_from": goal.valid_from.strftime("%Y-%m-%d %H:%M:%S"),
										"valid_to": goal.valid_to.strftime("%Y-%m-%d %H:%M:%S"),"value":goal.value,
										"frequency": goal.frequency}
		return jsonify(goal_dict)
	else:
		return jsonify({})	

@app.route("/settings")
def settings():
	print "session=", session
	if session.get("user_id"):
		user = User.query.get(session["user_id"])
		return render_template("settings.html", user=user)
	else:
		flash("You must be logged in to view this")
		return redirect("/login")	

@app.route("/update_settings.json", methods = ["POST"])
def update_settings():
	if session.get("user_id"):
		user = User.query.get(session["user_id"])
		email = request.form.get("email", None)
		password = request.form.get("password", None)
		old_password = request.form.get("old_password", None)
		if password and user.password != old_password:
			return jsonify(None)
		print email
		user.update_setting(email=email, password=password)
		print user.email, user.password
		return jsonify({"email": user.email, "password": user.password})
	else:
		return jsonify(None)	


@app.route("/enter_sleep")
def enter_sleep():
	fhf.check_session()
	return render_template("enter_sleep.html")

@app.route("/enter_sleep", methods=["POST"])
def record_sleep():
	fhf.check_session()
	bedtime = request.form.get("bedtime")
	waketime = request.form.get("waketime")
	user = User.query.get(session["user_id"])
	sleep_goals = user.get_current_sleep_goals()
	for goal in sleep_goals:
		SleepStatus.save_sleep_goal_status(goal,bedtime, waketime, frequency=goal.frequency)
		print bedtime, type(bedtime), dir(bedtime)
	return redirect("user/%s"%user.username)
	