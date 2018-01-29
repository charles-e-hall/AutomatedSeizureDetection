#This library will extract data from the Nicolet binary file
#for a specified event.
#The event is supplied as a timestamp that was extracted
#from the human scoring xlsx using EEGUtils
#The timestamps are pulled from the AWS MySQL table
#The data is returned as an array

import array
import struct

class Nicolet:
	def __init__(self, filename):
		self.f = open(filename, 'rb')
		self.header = array.array('c', '\0' * 2000)


#Random notes


buff = array.array('c', '\0' * len(header))

for i in range(len(header)):
	struct.pack_into('<c', buff, i, header[i])

