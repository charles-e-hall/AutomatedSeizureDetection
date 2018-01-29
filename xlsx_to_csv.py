#This script will convert the xlsx files containing the human expert scoring 
#to csv files for further processing

import xlrd
import csv
import sys
import os

def xlsxConvert(orig_path, excelWB, sheetname, destinationFolder):
    
	# if sys.argv[1]:
	# 	destinationFolder = sys.argv[1]
	# else:
	# 	destinationFolder = str(os.getcwd())
	excelFile = orig_path + '/' + excelWB
    wb = xlrd.open_workbook(excelFile)
    sh = wb.sheet_by_name(sheetname)
    destinationFile = destinationFolder + excelWB.split('.')[-2] + '.csv'
    csvFile = open(destinationFile, 'w')
    wr = csv.writer(csvFile, quoting=True)
    
    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))
        
    csvFile.close()

def createFileList(path):
	fileList = []
	pathList = []

	for (dirpath, dirname, filename) in os.walk(path):
		if str(filename).split('.')[-1] == "xlsx']":
			fileList.append(filename)
			pathList.append(dirpath)

	return pathList, fileList

if __name__ == "__main__":
	orig_path = '/Volumes/dusom_mcnamaralab/all_staff/Charlie/EEG Predictions/ExcelFiles/DylanExpt5'
	save_path = '/Volumes/dusom_mcnamaralab/all_staff/Charlie/EEG Predictions/ExcelFiles/CSV/'

	paths, files = createFileList(orig_path)
	for i in range(len(files)):
		fname = orig_path + '/' + files[i]
		xlsxConvert(fname, 'Sheet1', save_path)

