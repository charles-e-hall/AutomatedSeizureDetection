import eeglib
import os

def createFileList(path):
	fileList = []
	pathList = []

	for (dirpath, dirname, filename) in os.walk(path):
		if str(filename).split('.')[-1] == "bin']":
			fileList.append(filename)
			pathList.append(dirpath)

	return pathList, fileList


def trainingData(path, files, outFile, label):
	for i in files:
		fname = path + i
		eventHandler = eeglib.Event(fname)
		eventHandler.filterData('notch', 60)
		eventHandler.createTrainingData(outFile, 4, [label])

TestPaths, TestFiles = createFileList('/Volumes/dusom_mcnamaralab/all_staff/Charlie/NicoletEventFiles/')
ConPaths, ConFiles = createFileList('/Volumes/dusom_mcnamaralab/all_staff/Charlie/NicoletControlFiles/')

trainingData(TestPaths[0], TestFiles[0], '/Volumes/dusom_mcnamaralab/all_staff/Charlie/NicoletTrainingData/TrainingData.dat', 1)
trainingData(ConPaths[0], ConFiles[0], '/Volumes/dusom_mcnamaralab/all_staff/Charlie/NicoletTrainingData/TrainingData.dat', 0)


