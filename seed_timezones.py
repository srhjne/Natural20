from pytz import all_timezones


with open("timezones.dat", "w") as f:
	for timezone in all_timezones:
		f.write(timezone+"\n")


		