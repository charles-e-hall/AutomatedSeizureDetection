import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import eeglib
import sys



def update(val):
	pos = spos.val
	ax.axis([pos, pos+10, -1500, 1500])
	fig.canvas.draw_idle()


# def plotEvent(suffix, events):
# 	for num in [events]:
# 		path = '/Volumes/dusom_mcnamaralab/all_staff/Charlie/NicoletEventFiles/Patient8t{}_Event{}.bin'.format(suffix, num)
# 		fh = eeglib.Event(path)
# 		fh.filterData('notch', 60)
# 		t = np.linspace(0, fh.length/500, fh.length)
# 		fig, ax = plt.subplots(1,1)
# 		axpos = plt.axes([0.2, 0.1, 0.65, 0.03])
# 		spos = Slider(axpos, 'Pos', 0.1, 90.0)

# 		spos.on_changed(update(spos, fig, ax))
# 		plt.show()

if __name__ == '__main__':
	path = '/Volumes/dusom_mcnamaralab/all_staff/Charlie/NicoletEventFiles/Patient8t{}_Event{}.bin'.format(sys.argv[1], sys.argv[2])
	fh = eeglib.Event(path)
	fh.filterData('notch', 60)
	t = np.linspace(0, fh.length/500, fh.length)
	fig, ax = plt.subplots(1,1)

	plt.subplots_adjust(bottom=0.25)
	plt.axis([0, 10, -1500, 1500])
	axcolor = 'lightgoldenrodyellow'
	axpos = plt.axes([0.2, 0.1, 0.65, 0.03], axisbg=axcolor)
	spos = Slider(axpos, 'Pos', 0.1, t[-1])

	spos.on_changed(update)
	ax.plot(t, fh.chan4)
	plt.show()