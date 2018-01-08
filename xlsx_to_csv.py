#This script will convert the xlsx files containing the human expert scoring 
#to csv files for further processing

import xlrd
import csv
import sys
import os

def xlsxConvert(excelWB, sheetname, destinationFolder):
    
	if sys.argv[1]:
		destinationFolder = sys.argv[1]
	else:
		destinationFolder = str(os.getcwd())

    wb = xlrd.open_workbook(excelWB)
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

