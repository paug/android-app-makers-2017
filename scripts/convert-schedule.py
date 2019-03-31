"""
Convert the schedule JSON used on website to adapted format for app.
source: https://github.com/paug/android-makers-2019/blob/master/data/database/schedule.json
"""

#!/usr/bin/env python

import json
from datetime import datetime

input_schedule_raw = "schedule.json"
output_schedule_app = "schedule-app.json"

rooms = ["moebius", "blin", "202", "204"]

talks = []

def convertDate(datetime_str):
	# TODO set timezone too
	raw_date = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
	return raw_date.isoformat()

def extractTalks(day_str, timeslots):
	for slot in timeslots_day_1:
		start_date_string = "%s %s" % (day_str, slot["startTime"])
		end_date_string = "%s %s" % (day_str, slot["startTime"])

		sessions = slot["sessions"]
		if (len(sessions) == 1):
			talk = {}

			items = sessions[0]["items"]
			talk["startDate"] = convertDate(start_date_string)
			talk["endDate"] = convertDate(start_date_string)
			talk["roomId"] = "all"
			talk["sessionId"] = items[0]
			talks.append(talk)
		if (len(sessions) == 4):
			for session in sessions:
				items = session["items"]
				session_index = sessions.index(session)

				if (len(items) > 0):
					talk = {}
					talk["startDate"] = convertDate(start_date_string)
					talk["endDate"] = convertDate(start_date_string)
					talk["roomId"] = rooms[session_index]
					talk["sessionId"] = items[0]
					if (session.get("extend") != None):
						# TODO Change the end time
						talk["extend"] = session["extend"]
					talks.append(talk)

with open(input_schedule_raw) as json_data:
	schedule = json.load(json_data)
	day_1 = schedule["2019-04-23"]
	day_2 = schedule["2019-04-24"]

	timeslots_day_1 = day_1["timeslots"]
	timeslots_day_2 = day_2["timeslots"]

	extractTalks("2019-04-23", timeslots_day_1)
	extractTalks("2019-04-24", timeslots_day_2)
	
with open(output_schedule_app, 'wb') as outfile:
	json.dump(talks, outfile, sort_keys=True, indent=4)