#This script will read events from the nicolet_event_log table and extract the data
#from the Nicolet file and store the exported data in a NoSQL database

import MySQLdb
import matlab.engine

