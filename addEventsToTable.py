#This script uses EEGUtils.py to create the event log table and then add events to it

import os
import settings
import EEGUtils



def createFileList(path):
	fileList = []
	pathList = []

	for (dirpath, dirname, filename) in os.walk(path):
		if str(filename).split('.')[-1] == "csv']":
			fileList.append(filename)
			pathList.append(dirpath)

	return pathList, fileList



if __name__ == "__main__":
	settings.init()
	#EEGUtils.makeEventTable(settings.DB_ENDPOINT, settings.DB_PORT, settings.DB_USER, settings.DB_PASSWORD, settings.DB_NAME)
	save_path = '/Volumes/dusom_mcnamaralab/all_staff/Charlie/EEG Predictions/ExcelFiles/CSV/'
	paths, files = createFileList(save_path)

	if len(paths) != len(files):
		print "There is a mismatch in length between paths and files"

	totalSeizures = 0

	for i in range(len(files)):
		fname = paths[0] + '/' + files[0][i]
		for j in range(7):
			df = EEGUtils.returnDataBlock(fname, j)
			seizures = EEGUtils.getSeizuresFromBlock(df)
			totalSeizures += len(seizures)
			print "Filename is {} and data block is {}\n".format(fname, j)
			EEGUtils.insertEvents(seizures, settings.DB_ENDPOINT, settings.DB_PORT, settings.DB_NAME, settings.DB_USER, settings.DB_PASSWORD)

	print "\nAddition of events is complete.\nThere were {} seizure events added to the table.\n".format(totalSeizures)