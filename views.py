from server import app, flow #, JS_TESTING_MODE
# from oauth2client.client import OAuth2WebServerFlow
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage

from flask import jsonify, render_template, redirect, request, flash, session, g

from model import db, User, Goal, GoalStatus, UserStatus, Monster, Attack, LevelLookup, SleepStatus, Friendship, Team, UserTeam, TeamInvite

import os
import datetime
import random
import pytz

import fitness_helper_functions as fhf
import dnd_helper_functions as dhf

import bcrypt

@app.before_request
def check_login_time():
	if request.path not in ('/','/login', '/logout', '/registration','/clock.json','/static/styles.css', '/static/DUNGRG__.TTF', '/static/d20-navbar.png'):
		if session.get("login_time", None) and session.get("user_id", None):
			if (datetime.datetime.now() - session.get("login_time")).total_seconds() > 60*60:
				flash("Your session has timed out, please log in again")
				del session["user_id"]
				return redirect("/login")
		else:
			flash("Please log in to view this")
			return redirect("/login")
	g.jasmine_tests = False
	print "jasmine", g.jasmine_tests

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
	is_friend = user.check_friendship(session.get("user_id"))
	if session.get("user_id", "") != user.user_id and not is_friend:
		flash("You must be friends with %s to view their page"% username)
		return redirect("/") 
	else:
		now = datetime.datetime.now()
		status = user.get_current_status()

		xp = status.current_xp
		hp = status.current_hp
		if hp == 0 and not is_friend:
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
						progresses.append([pytz.utc.localize(progress.date_recorded).astimezone(pytz.timezone(user.timezone)).strftime("%I:%M%p %B %d, %Y"), round(mean_value/(60.0*60),2), min(100.0*mean_value/goal.value,100), goal])
					else:
						progresses.append([pytz.utc.localize(progress.date_recorded).astimezone(pytz.timezone(user.timezone)).strftime("%I:%M%p %B %d, %Y"), round(mean_value,2), min(100.0*mean_value/goal.value,100), goal])
				else:
					progress = goal.get_current_status()
					if goal.goal_type == "Sleep":
						progresses.append([pytz.utc.localize(progress.date_recorded).astimezone(pytz.timezone(user.timezone)).strftime("%I:%M%p %B %d, %Y"), progress.value/(60.0*60), min(100.0*progress.value/goal.value,100), goal])
					else:
						progresses.append([pytz.utc.localize(progress.date_recorded).astimezone(pytz.timezone(user.timezone)).strftime("%I:%M%p %B %d, %Y"), progress.value, min(100.0*progress.value/goal.value,100), goal])


			return render_template("user_page.html", username=username,  
				                   goalstatus = progresses, xp=xp, hp=hp, level=level, isfriend=is_friend)


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
	if code:
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
	else:
		flash("You need to allow access to Google Fit to access all the features")
		flash("You will only be able to track Sleep goals")
		user = User.query.get(int(session.get("user_id")))
		if user.get_unresolved_overdue_goals():
			print "Unresolved goals", user.get_unresolved_overdue_goals()
			return redirect("/outcome")
		else:			
			return redirect("/user/%s" % user.username)


@app.route('/outcome.json')
def outcome_json():
	user = User.query.get(int(session.get("user_id")))
	goal_list = dhf.get_outcome_dict(user)
	print goal_list
	return jsonify(goal_list)



@app.route('/outcome')
def outcome():
	return render_template("outcome.html")


@app.route('/set_goal', methods=['GET'])
def set_goals():
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
	user = User.query.get(session.get('user_id'))
	goal_type = request.form.get("goal_type")
	goal_value = request.form.get("value")
	goal_value = int(goal_value)
	valid_from_u = request.form.get("valid_from")
	valid_from = pytz.timezone(user.timezone).localize(datetime.datetime.strptime(valid_from_u, "%Y-%m-%d")).astimezone(pytz.utc)
	valid_to_u = request.form.get("valid_to")
	valid_to = pytz.timezone(user.timezone).localize(datetime.datetime.strptime(valid_to_u, "%Y-%m-%d")).astimezone(pytz.utc)
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
		if bcrypt.hashpw(password.encode('utf8'), user.password.encode('utf8')) == user.password:
			messages = user.get_team_messages()
			for message in messages:
				flash(message)
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
	if session.get("user_id", None):
		del session["user_id"]
	flash("You are now logged out")
	return redirect("/login")


@app.route("/goal_graph.json")
def goal_graph():
	page_user = request.args.get("username")
	
	if session.get("user_id"):
		user = User.query.get(session["user_id"])
		if page_user:
			user = User.query.filter(User.username == page_user).first()
		goals = user.get_current_goals()
		goal_dict = {}
		for goal in goals:
			if goal.frequency == "Daily":
				series = goal.get_daily_status_series()
				print series
			else:
				series = goal.get_status_series()
				print series
			goal_dict[goal.goal_id] = {"series": series, "valid_from": pytz.utc.localize(goal.valid_from.strftime("%Y-%m-%d %H:%M:%S")).astimezone(pytz.timezone(user.timezone)),
										"valid_to": pytz.utc.localize(goal.valid_to.strftime("%Y-%m-%d %H:%M:%S")).astimezone(pytz.timezone(user.timezone)),"value":goal.value,
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
	user = User.query.get(session["user_id"])
	email = request.form.get("email", None)
	password = request.form.get("password", None)
	old_password = request.form.get("old_password", None)
	if password and bcrypt.hashpw(old_password.encode('utf8'),user.password.encode('utf8')) != user.password:
		return jsonify(None)
	print email
	user.update_setting(email=email, password=str(password))
	print user.email, user.password
	return jsonify({"email": user.email, "password": user.password})
		


@app.route("/enter_sleep")
def enter_sleep():
	return render_template("enter_sleep.html")

@app.route("/enter_sleep", methods=["POST"])
def record_sleep():
	bedtime = request.form.get("bedtime")
	waketime = request.form.get("waketime")
	user = User.query.get(session["user_id"])
	sleep_goals = user.get_current_sleep_goals()
	for goal in sleep_goals:
		SleepStatus.save_sleep_goal_status(goal,bedtime, waketime, frequency=goal.frequency)
		print bedtime, type(bedtime), dir(bedtime)
	return redirect("user/%s"%user.username)



@app.route("/add_friends")
def add_friends():
	return render_template("add_friends.html")


@app.route("/users.json")
def search_users():
	user = User.query.get(session.get("user_id"))
	search_term = request.args.get("search_term")
	search = db.session.query(User.user_id, User.username)
	search_users = search.filter(User.user_id != session["user_id"], User.username.like("%{}%".format(search_term))).all()
	result = [(user_id, username, user.check_friendship(user_id), user.check_pending_friend_request(user_id)) for (user_id, username) in search_users]			   
	return jsonify(result)
	

@app.route("/add_friend.json", methods=["POST"])
def add_friend():
	friend_id = request.form.get("user_id")
	user_id = session.get("user_id")
	user = User.query.get(user_id)
	fr = user.get_sent_friend_requests()
	if user.check_friendship(friend_id):
		return jsonify(False)
	elif user.check_pending_friend_request(friend_id):
		return jsonify(False)
	else:
		friendship = Friendship(user_id_1=user_id, user_id_2=friend_id, verified=False)
		db.session.add(friendship)
		db.session.commit()
		fs = Friendship.query.filter(Friendship.user_id_1==user_id, Friendship.user_id_2 == friend_id).all()
		return jsonify("success")


@app.route("/friend_request.json")
def friend_request():
	user = User.query.get(session["user_id"])
	friend_requests = user.get_friend_requests()
	print friend_requests
	return jsonify([{"friendship_id": friendship.friendship_id,
					 "friend_name": user.username,
					 "friend id": user.user_id} for friendship, user in friend_requests])


@app.route("/friend_request.json", methods=["POST"])
def friend_request_accept():
	friendship_id = request.form.get("friendship_id")
	friendship = Friendship.query.get(friendship_id)
	friendship.verified = True
	db.session.commit()
	return jsonify([friendship_id])

@app.route("/friends")
def friends():
	user = User.query.get(session.get("user_id"))
	friends = user.get_friends()
	print friends
	return render_template("friends.html", friends=friends)

@app.route("/team")
def team():
	return render_template("team.html")

@app.route("/get_leaderboard.json")
def leaderboard():
	xp_team = dhf.get_team_rankings(dictionary=True)
	return jsonify(xp_team)

@app.route("/get_team.json")
def get_team():
	teamname = request.args.get("teamname")
	user = User.query.get(session["user_id"])
	print "teamname", teamname 
	if teamname == "":
		team = user.get_current_team()
		print "my team is", team
		if not team:
			return jsonify([])
	else:
		team = Team.query.filter(Team.teamname == teamname).first()
	current_team_dict = {}
	if team:
		users = team.get_current_team_members()
		for user in users:
			status = user.get_current_status()
			current_team_dict[user.user_id] = {"username": user.username, "xp": status.current_xp,
											    "hp": status.current_hp, "level": status.level}
	return jsonify([team.teamname, current_team_dict]) 

@app.route("/get_friends.json")
def get_friends():
	user = User.query.get(session["user_id"])
	friends = user.get_friends()
	print friends
	friendname_list = [ friend[0].username for friend in friends]
	return jsonify(friendname_list)

@app.route("/leave_team.json", methods=["POST"])
def leave_team():
	user = User.query.get(session["user_id"])
	team = user.get_current_team()
	teamname = request.form.get("teamname")
	print "teamname from react", teamname
	print "teamname from user", team.teamname
	if teamname != team.teamname:
		return jsonify(False)
	else:
		return jsonify(user.leave_current_team())


@app.route("/invite_friend.json", methods=["POST"])
def invite_friends():
	user = User.query.get(session["user_id"])
	team = user.get_current_team()
	friendname = request.form.get("friendname")
	friend = User.query.filter(User.username == friendname).first()
	print "I am in invite friends"
	print user, team, friend
	if not friend:
		return jsonify(False)
	if friend.get_current_team() == team:
		return jsonify("%s is already a member of %s"%(friend.username, team.teamname))
	current_invite = TeamInvite.query.filter(TeamInvite.user_id==friend.user_id, TeamInvite.resolved==False, TeamInvite.team_id==team.team_id).all()
	if current_invite:
		return jsonify("%s has already been invited to %s"%(friend.username, team.teamname))
	teaminvite = TeamInvite(inviter_id = user.user_id, user_id=friend.user_id, resolved=False, team_id=team.team_id)
	db.session.add(teaminvite)
	db.session.commit()
	return jsonify("%s was invited to join %s"%(friend.username, team.teamname))

@app.route("/get_team_requests.json")
def get_team_requests():
	user = User.query.get(session["user_id"])
	team_requests = user.get_team_requests()
	if not team_requests:
		return jsonify([])
	json_list = []
	for invite in team_requests:
		if invite.resolved == False:
			inviter = User.query.get(invite.inviter_id)
			json_list.append({"invite_id":invite.invite_id,"inviter_name": inviter.username, "teamname":invite.team.teamname})

	return jsonify(json_list)

@app.route("/join_team.json", methods=["POST"])
def join_team():
	user = User.query.get(session["user_id"])
	teamname = request.form.get("teamname")
	invite_id = request.form.get("invite_id")
	if not teamname or not invite_id:
		return jsonify(False)
	teamrequest = TeamInvite.query.get(invite_id)
	team = Team.query.filter(Team.teamname == teamname).first()
	if not team:
		return jsonify(False)
	user.join_team(team.team_id) 
	new_team = user.get_current_team()
	teaminvite = TeamInvite.query.get(invite_id)
	teaminvite.resolved = True
	db.session.commit()
	return jsonify({"teamname": new_team.teamname})


@app.route("/make_new_team.json", methods=["POST"])
def make_new_team():
	user = User.query.get(session["user_id"])
	teamname = request.form.get("teamname")
	team_check = Team.query.filter(Team.teamname == teamname).all()
	print "team_check", team_check
	if len(team_check) > 0:
		return jsonify(False)
	else:
		user.leave_current_team()
		team = Team.create_team(teamname=teamname, user_id=user.user_id)

	return jsonify({"teamname": team.teamname})

@app.route("/clock.json")
def clock():

	if session.get("user_id"):
		user = User.query.get(session["user_id"])
		timezone = user.timezone
	else:
		timezone = "US/Pacific"
	return jsonify(datetime.datetime.strftime(datetime.datetime.now(pytz.timezone(timezone)),"%d %B %Y"))

