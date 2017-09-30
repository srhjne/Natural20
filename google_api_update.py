import fitness_helper_functions as fhf 
from model import User, db, connect_to_db

from apiclient.discovery import build
from oauth2client.file import Storage
import httplib2

import time

from server import app



def main():
	for user in User.query.all():
		print user
		storage = Storage('credentials%s.dat'%user.user_id)

		# The get() function returns the credentials for the Storage object. If no
		# credentials were found, None is returned.
		credentials = storage.get()

		# If no credentials are found or the credentials are invalid due to
		# expiration, new credentials need to be obtained from the authorization
		# server. The oauth2client.tools.run_flow() function attempts to open an
		# authorization server page in your default web browser. The server
		# asks the user to grant your application access to the user's data.
		# If the user grants access, the run_flow() function returns new credentials.
		# The new credentials are also stored in the supplied Storage object,
		# which updates the credentials.dat file.
		if credentials and not credentials.invalid:
			# Create an httplib2.Http object to handle our HTTP requests, and authorize it
			# using the credentials.authorize() function.
			http = httplib2.Http()
			http = credentials.authorize(http)

			# The apiclient.discovery.build() function returns an instance of an API service
			# object can be used to make API calls. The object is constructed with
			# methods specific to the calendar API. The arguments provided are:
			#   name of the API ('calendar')
			#   version of the API you are using ('v3')
			#   authorized httplib2.Http() object that can be used for API calls
			service = build('fitness', 'v1', http=http)
			print fhf.update_goal_status(user, service)
			



connect_to_db(app)
db.create_all()
while True:
	time.sleep(15*60)
	try:
		main()
	except Exception:
		continue
