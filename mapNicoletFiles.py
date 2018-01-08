#This script walks through directories finding Nicolet EEG files
#and inserting the file name and path into an AWS SQL table for 
#accessing by future scripts.

import os
import MySQLdb
import sys

#Use command line argument of 1 to drop the table and re-create it
if sys.argv[1]:
	db = MySQLdb.connect(host='eeg.cpivbi1tmjzn.us-east-2.rds.amazonaws.com', port=3306, user='charlie', passwd='Standard01', db='eegevents')
	h = db.cursor()
	sql1 = "DROP TABLE IF EXISTS nicolet_file_map; CREATE TABLE nicolet_file_map (hard_drive VARCHAR(255), path VARCHAR(255), filename VARCHAR(255)); COMMIT;"
	h.execute(sql1)
	db.close()

def getNicoletFiles(path):
    allFiles = []
    allPaths = []
    nicoletFiles = []
    nicoletPaths = []

    for (dirpath, dirname, filename) in os.walk(path):
        allFiles.append(filename)
        allPaths.append(dirpath)
        
    for i in range(len(allFiles)):
        if str(allFiles[i]).split('.')[-1] == "e']":
            nicoletFiles.append(allFiles[i][0])
            nicoletPaths.append(allPaths[i])
            
    del allFiles, allPaths
    return nicoletPaths, nicoletFiles


paths, files = getNicoletFiles('/Volumes/TOSHIBA EXT/pY816 DM Experiment 5')

DB = MySQLdb.connect(host='eeg.cpivbi1tmjzn.us-east-2.rds.amazonaws.com', port=3306, user='charlie', passwd='Standard01', db='eegevents')

handle = DB.cursor()
hardDrive = 'Keshov CPU 2'

for i in range(len(paths)):
    sql = "INSERT INTO nicolet_file_map VALUES ('{}', '{}', '{}');".format(hardDrive, paths[i], files[i])
    handle.execute(sql)

handle.execute("COMMIT;")

DB.close()