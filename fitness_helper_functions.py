import datetime
import time
from model import GoalStatus, Goal, db, SleepStatus
from flask import session, redirect

def get_last_week_millis():
	""" gets the milliseconds from epoch for the last week """
	day =datetime.datetime.now().day
	month = datetime.datetime.now().month
	year = datetime.datetime.now().year
	datestring = ("%0d %0d %0d")%(day,month, year)
	struct_time = time.strptime(datestring, "%d %m %Y")
	millisnow = int(round(time.mktime(struct_time) * 1000))+86400000
	millislast_week = millisnow - 7*86400000
	return millisnow, millislast_week


def get_millis_date(datetime1):
	""" Takes in a datetime object and returns milliseconds from epoch """
	return int(round(time.mktime(datetime1.timetuple()) * 1000))
	
def get_aggregate(goal, service, enddate=None):
	if not enddate:
		enddate = goal.valid_to
	millisstart = get_millis_date(goal.valid_from)
	millisend = get_millis_date(enddate)
	if goal.frequency == "Daily":
		delta = 1000*60*60*24
	else:
		delta = millisend - millisstart

	if goal.goal_type == "Steps":
		aggregateBy = [{
			    	"dataTypeName": "com.google.step_count.delta",
			    	"dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
			  		}]
	elif goal.goal_type == "Calories":
		aggregateBy = [{"dataTypeName": "com.google.calories.expended"}]
	agg = service.users().dataset().aggregate(userId="me",
						body={"aggregateBy":aggregateBy,
			  		"bucketByTime": { "durationMillis": delta }, # This is 24 hours
			  		"startTimeMillis": millisstart, #start time
			  		"endTimeMillis": millisend # End Time
			  		})
	return agg


def update_goal_status(user, service):
	goals = user.get_unresolved_goals()
	for goal in goals:
				if goal.goal_type not in ("Steps", "Calories"):
					continue
				print goal
				most_recent_status = goal.get_current_status()
				last_3days = goal.get_status_last_3days()
			# if goal.goal_type == "Steps":
				for status in last_3days:
					agg = get_aggregate(goal, service, status.date_recorded)
					if len(agg.execute()['bucket']) != 0 and len(agg.execute()['bucket'][-1]['dataset'][0]['point']) != 0:
						if goal.goal_type == "Steps":
							column = "intVal"
						elif goal.goal_type == "Calories":
							column = "fpVal"
					#print "Hooray you have done %s Steps" % agg.execute()['bucket'][0]['dataset'][0]['point'][0]['value'][0]['intVal']
						value = agg.execute()['bucket'][-1]['dataset'][0]['point'][0]['value'][0][column]
						if value > status.value:
							status.value = value
							db.session.commit()
				agg = get_aggregate(goal, service, datetime.datetime.now())
				print "Got to here"	
				if len(agg.execute()['bucket']) != 0 and len(agg.execute()['bucket'][-1]['dataset'][0]['point']) == 0:
					return "No data"
				else:
					if goal.goal_type == "Steps":
						column = "intVal"
					elif goal.goal_type == "Calories":
						column = "fpVal"
					print "got to the second bit"
					#print "Hooray you have done %s Steps" % agg.execute()['bucket'][0]['dataset'][0]['point'][0]['value'][0]['intVal']
					value = agg.execute()['bucket'][-1]['dataset'][0]['point'][0]['value'][0][column]
					print value, most_recent_status.value
					if most_recent_status.value != value:
						goalprogress = GoalStatus(goal_id = goal.goal_id, date_recorded = datetime.datetime.now(), value=value)
						print value
						db.session.add(goalprogress)
						db.session.commit()


def set_goal(user, goal):
	db.session.add(goal)
	db.session.commit()
	goal_db = Goal.query.filter(Goal.user_id==user.user_id, Goal.xp==xp, Goal.goal_type==goal_type, Goal.value==goal_value, Goal.valid_from==valid_from, Goal.valid_to==valid_to).first()
	goalstatus = GoalStatus(goal_id=goal_db.goal_id,value=0,date_recorded=goal.valid_from)
	db.session.add(goalstatus)
	db.session.commit()

def check_session():
	if not session.get("user_id"):
		flash("You must be logged in to view this")
		return redirect("/login")






