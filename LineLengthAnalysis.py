import os
import eeglib
from matplotlib import pyplot as plt
import numpy as np

path = '/Volumes/dusom_mcnamaralab/all_staff/Charlie/NicoletEventFiles/'

files = []

for (dirpath, dirname, filename) in os.walk(path):
    if filename[0].split('.')[-1] == 'bin':
        files.append(filename)

        
files = files[0]
#print files
#del files[2]
#print files


c4 = []

for fname in files:
    fullFile = path + str(fname)
    print fname
    fh = eeglib.Event(fullFile)
    fh.filterData('notch', 60)
    #f, ax = plt.subplots(1,2)
    #ax[0].plot(fh.chan3)
    #ax[1].plot(fh.chan4)
    #c1.append(fh.lineLength(1))
    #c2.append(fh.lineLength(2))
    #fh.power(3)
    #fh.power(4)
    #c3.extend(fh.lineLength(3))
    c4.extend(fh.lineLengthFractal(4, windowSize=10))
    


path = '/Volumes/dusom_mcnamaralab/all_staff/Charlie/NicoletControlFiles/'

controlFiles = []

for (dirpath, dirname, filename) in os.walk(path):
    if filename[0].split('.')[-1] == 'bin':
        controlFiles.append(filename)


controlFiles = controlFiles[0]
#print files
#del files[2]
#print controlFiles

cc4 = []
for fname in controlFiles:
    fullFile = path + str(fname)
    print fname
    fh = eeglib.Event(fullFile)
    fh.filterData('notch', 60)
    #f, ax = plt.subplots(1,2)
    #ax[0].plot(fh.chan3)
    #ax[1].plot(fh.chan4)
    #c1.append(fh.lineLength(1))
    #c2.append(fh.lineLength(2))
    #fh.power(3)
    #fh.power(4)
    #cc3.extend(fh.lineLength(3))
    cc4.extend(fh.lineLengthFractal(4, windowSize=10))

    scale = np.linspace(-3,3,200)

c3Percent = []
c4Percent = []

for i in range(len(scale)):
    threshold = np.mean(cc4) - scale[i]*np.std(cc4)
    c3Percent.append(100*len([x for x in cc4 if x>=threshold])/float(len(cc4)))
    c4Percent.append(100*len([y for y in c4 if y>=threshold])/float(len(cc4)))
    
    
plt.plot(c3Percent, c4Percent)
plt.xlim((0,100))
plt.ylim((0,100))
plt.ylabel('Percent of Events Detected (%)')
plt.xlabel('False Positive Rate (%)')
plt.title('Performance of Line Length on McNamara Lab EEG')
plt.plot((0,100), (0,100), 'r')
plt.savefig('LineLengthPerformance10secWindowNoBuffer.eps', format='eps')

plt.hist(cc4, 20, facecolor='b', normed=True, label='Normal EEG')
plt.hist(c4, 20, facecolor='r', normed=True, label='Seizure Event')
plt.legend()
plt.title('Distribution of Line Lenght (5sec Window)')
plt.ylabel('Percent of Events')
plt.xlabel('Line Length')
plt.savefig('DistributionofLineLength10secWindow.png', format='png')