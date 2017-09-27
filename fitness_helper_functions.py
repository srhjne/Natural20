import datetime
import time

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
	



