#This script will read events from the nicolet_event_log table and extract the data
#from the Nicolet file and store the exported data in a NoSQL database

import MySQLdb
import matlab.engine
import settings
import numpy as np

settings.init()

db = MySQLdb.connect(host=settings.DB_ENDPOINT, port=settings.DB_PORT, user=settings.DB_USER, passwd=settings.DB_PASSWORD, db=settings.DB_NAME)
handle = db.cursor()

handle.execute("SELECT * FROM nicolet_event_log")

events = list(handle)
path = []
file = []
print "There are {} events to extract.\n".format(len(events))

for i in range(len(events)):
	fname = events[i][1] + '.e'
	sql = "SELECT * FROM nicolet_file_map WHERE filename='{}'".format(fname)
	handle.execute(sql)
	out = list(handle)
	if len(out) > 1:
		print "\nMore than one row returned from nicolet_file_map table\n"

	path.append(out[0][1])
	file.append(out[0][2])

db.close()

if len(path) != len(events):
	print "\nThere is a mismatch in length between paths and events\n"

eng = matlab.engine.start_matlab()

for i in range(len(path)):
	source_path = path[i] + '/' + file[i]
	dest_path = '/Volumes/dusom_mcnamaralab/all_staff/Charlie/NicoletEventFiles/' + events[i][1] + '_Event{}.bin'.format(i)
	start = (int(events[i][4].split(':')[0]), int(events[i][4].split(':')[1]), int(events[i][4].split(':')[2]))
	stop = (int(events[i][5].split(':')[0]), int(events[i][5].split(':')[1]), int(events[i][5].split(':')[2]))
	eng.NicoletToBinary(source_path, dest_path, start, stop, 60, nargout=0)
	print "\nNicolet Event Written: {}".format(i)

eng.quit()


