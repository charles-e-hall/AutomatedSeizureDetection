#This library will contain functions for creating seizure event classes and methods
#for implementing basic traditional seizure detection methods
import struct
import numpy as np
from scipy import signal
import numpy as np
from matplotlib import pyplot as plt
#%matplotlib inline


class Event():
    def __init__(self, filename):
        self.fh = open(filename, 'r')
        self.length = struct.unpack('<Q', self.fh.read(8))[0]
        self.channel = struct.unpack('<B', self.fh.read(1))[0]
        #self.channel_ref = {'T4' = 13, 'C4' = 6, 'F7' = 11, 'F3' = 3, 'F4' = 4, 'FP2' = 2, 'Cz' = 17, 'P3' = 7}
        self.montage = {'Chan1':('T4', 'C4'), 'Chan2':('F7', 'F3'), 'Chan3':('F4', 'FP2'), 'Chan4':('Cz', 'P3')}
        self.filename = filename.split('/')[-1]

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


    def lineLength(self, channel, windowSize=1):
        self.lineLengthArray = []
        for j in range(1, self.length/500):
            self.totalLineLength = 0
            data3 = self.chan3[500*(j-1):500*windowSize*j]
            data4 = self.chan4[500*(j-1):500*windowSize*j]
            for i in range(1, windowSize*500):
                if channel == 1:
                    self.totalLineLength += abs(self.chan1[i] - self.chan1[i-1])
                elif channel == 2:
                    self.totalLineLength += abs(self.chan2[i] - self.chan2[i-1])
                elif channel == 3:
                    self.totalLineLength += abs(data3[i] - data3[i-1])
                elif channel == 4:
                    self.totalLineLength += abs(data4[i] - data4[i-1])
                else:
                    self.totalLineLength = 0
            self.lineLengthArray.append(self.totalLineLength/500.)
    
        return self.lineLengthArray

    def lineLengthFractal(self, channel, windowSize=1):
        self.lineLengthArray = []
        for j in range(60, (self.length-60)/500):
            self.totalLineLength = 0
            data3 = self.chan3[500*(j-1):500*windowSize*j]
            data4 = self.chan4[500*windowSize*(j-1):500*windowSize*j]
            for i in range(1, windowSize*500):
                if channel == 1:
                    self.totalLineLength += abs(self.chan1[i] - self.chan1[i-1])
                elif channel == 2:
                    self.totalLineLength += abs(self.chan2[i] - self.chan2[i-1])
                elif channel == 3:
                    self.totalLineLength += abs(data3[i] - data3[i-1])
                elif channel == 4:
                    self.totalLineLength += abs(data4[i] - data4[i-1])
                else:
                    self.totalLineLength = 0
            self.lineLengthArray.append(np.log(self.totalLineLength)/np.log(500.))
    
        return self.lineLengthArray

    
    def readData(self, size):
        self.data = []
        for i in range(self.length):
            self.data.append(struct.unpack('<f', self.fh.read(size))[0])
        
        return self.data

    def filterData(self, type, fc, order=6, Q=30):
        if type == 'notch':
            self.b, self.a = signal.iirnotch(fc/(500./2.), Q)
        else:
            self.b, self.a = signal.butter(order, fc/(500./2.))

        self.chan1 = signal.filtfilt(self.b, self.a, self.chan1)
        self.chan2 = signal.filtfilt(self.b, self.a, self.chan2)
        self.chan3 = signal.filtfilt(self.b, self.a, self.chan3)
        self.chan4 = signal.filtfilt(self.b, self.a, self.chan4)
        
    def power(self, channel, windowSize=5):
        #Pre-allocate matrix of zeros 20xlength(range(5*500,self.length))
        self.power_matrix3 = np.zeros((20,len(range(1, self.length/500))))
        self.power_matrix4 = np.zeros((20,len(range(1, self.length/500))))
        #mul = len(range(5*500,self.length))/20
        for i in range(1, self.length/500):
            freq = np.arange(len(self.chan4[(i-1)*500:i*500]))*500/float(len(self.chan4[(i-1)*500:i*500]))
            sp4 = np.fft.fft(self.chan4[(i-1)*500:i*500])/len(self.chan4[(i-1)*500:i*500])
            sp3 = np.fft.fft(self.chan3[(i-1)*500:i*500])/len(self.chan3[(i-1)*500:i*500])
            m = (freq[-1] - freq[0])/float(len(self.chan4[(i-1)*500:i*500]))
            for j in range(1,20):
                self.power_matrix3[j-1,i-1] = sum(sp3.real[int(5*(j-1)/m):int(5*j/m)]**2)
                self.power_matrix4[j-1,i-1] = sum(sp4.real[int(5*(j-1)/m):int(5*j/m)]**2)
                
        #plt.figure(figsize=(5,10))
        #plt.matshow(self.power_matrix4, cmap=plt.cm.jet, fignum=1)
        self.power_matrix4[0:3,0:3] = 0
        self.power_matrix3[0:3,0:3] = 0
        plt.matshow(self.power_matrix4, cmap=plt.cm.jet)

    def createTrainingData(self, dataFile, channel, label, windowSize=5):
        self.numWindows = (len(self.chan4) - 120*500)/(windowSize*500)
        self.trainData = np.empty([windowSize*500+1, self.numWindows])
        #self.trainData = np.empty([self.numWindows, windowSize*500+1])
        fh = open(dataFile, 'a')
        for i in range(self.numWindows):
            start = 120*500 + i*windowSize*500
            stop = 120*500 + (i+1)*windowSize*500
            subline = self.chan4[start:stop]
            subline = np.append(subline, [label])
            self.trainData[:,i] = subline

        #print 'Shape of array to print: {} x {}\n'.format(np.shape(self.trainData))
        #print 'Shape of subline: {} x {}\n'.format(np.shape(subline))

        trainingDataOut = np.transpose(np.asarray(self.trainData))
        np.savetxt(fh, trainingDataOut, delimiter=',')
        fh.close()


    
        
        