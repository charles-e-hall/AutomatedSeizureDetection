#This library will contain functions for creating seizure event classes and methods
#for implementing basic traditional seizure detection methods
import struct
import numpy as np
from scipy import signal
import os

class Event():
	def __init__(self, filename):
		self.fh = open(filename, 'r')
		self.length = struct.unpack('<Q', self.fh.read(8))[0]
		self.channel = struct.unpack('<B', self.fh.read(1))[0]
		#self.channel_ref = {'T4' = 13, 'C4' = 6, 'F7' = 11, 'F3' = 3, 'F4' = 4, 'FP2' = 2, 'Cz' = 17, 'P3' = 7}
		self.montage = {'Chan1':('T4', 'C4'), 'Chan2':('F7', 'F3'), 'Chan3':('F4', 'FP2'), 'Chan4':('Cz', 'P3')}

		#Extract FP2
		self.fh.seek(self.length*4, 1)
		self.FP2 = self.readData(4)
		self.F3 = self.readData(4)
		self.F4 = self.readData(4)
		self.fh.seek(self.length*4, 1)
		self.C4 = self.readData(4)
		self.P3 = self.readData(4)
		self.fh.seek(self.length*4*3, 1)
		self.F7 = self.readData(4)
		self.fh.seek(self.length*4, 1)
		self.T4 = self.readData(4)
		self.fh.seek(self.length*4*3, 1)
		self.Cz = self.readData(4)
		self.chan1 = np.array(self.C4) - np.array(self.T4)
		self.chan2 = np.array(self.F3) - np.array(self.F7)
		self.chan3 = np.array(self.FP2) - np.array(self.F4)
		self.chan4 = np.array(self.P3) - np.array(self.Cz)


	def filterData(self, type, order, fc):
		if type == 'butter':
			self.b, self.a = signal.butter(order, fc/(500./2.))

		self.chan1 = signal.filtfilt(self.b, self.a, self.chan1)
		self.chan2 = signal.filtfilt(self.b, self.a, self.chan2)
		self.chan3 = signal.filtfilt(self.b, self.a, self.chan3)
		self.chan4 = signal.filtfilt(self.b, self.a, self.chan4)


	def lineLength(self, channel):
		self.totalLineLength = 0
		for i in range(1, self.length):
			if channel == 1:
				self.totalLineLength += abs(self.chan1[i] - self.chan1[i-1])
			elif channel == 2:
				self.totalLineLength += abs(self.chan2[i] - self.chan2[i-1])
			elif channel == 3:
				self.totalLineLength += abs(self.chan3[i] - self.chan3[i-1])
			elif channel == 4:
				self.totalLineLength += abs(self.chan4[i] - self.chan4[i-1])
			else:
				self.totalLineLength = 0

		self.totalLineLength = self.totalLineLength/self.length
        return self.totalLineLength

	def power(self, windowSize=5):
		#returns a powerMatrix with each row being a frequency band
		#and each column being a window position in time
		for i in range(len(self.chan4)):
			pass

	def entropy(self, windowSize=5):
		pass

	def readData(self, size):
		self.data = []
		for i in range(self.length):
			self.data.append(struct.unpack('<f', self.fh.read(size))[0])

		return self.data

	def createColormap(self, windowSize=5, powerMatrix):
		pass



# if __name__ == '__main__':
# 	path = '/Volumes/dusom_mcnamaralab/all_staff/Charlie/NicoletEventFiles/'

# 	files = []

# 	for (dirpath, dirname, filename) in os.walk(path):
# 		files.append(filename)

# 	files = files[0]
# 	c1 = []
# 	c2 = []
# 	c3 = []
# 	c4 = []

# 	for fname in files:
# 		fullFile = path + fname
# 		print fname, '\n'
# 		fh = Event(fullFile)
# 		fh.filterData('butter', 6, 50)
# 		c1.append(fh.lineLength(1))
# 		c2.append(fh.lineLength(2))
# 		c3.append(fh.lineLength(3))
# 		c4.append(fh.lineLength(4))


