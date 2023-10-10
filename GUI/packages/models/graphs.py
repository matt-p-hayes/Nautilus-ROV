import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from matplotlib import style
from datetime import datetime



from collections import deque

#matplotlib.rcParams.update({'font.size': 60})

style.use('ggplot')
#set(0,'defaultTextFontName','Courier')

starttime = datetime.now()
refresh_rate = 20

tmpr = 0
pres = 0
head = 0
time = 0

tmpr_prev = 0
pres_prev = 0
head_prev = 0
time_prev = 0

figure, (tmpr_subplot, pres_subplot, head_subplot) = plt.subplots(3)

figure.suptitle('Sensor Data')
tmpr_subplot.set_title('Temperature (C)', y = 1)
pres_subplot.set_title('Pressure (mbar)', y = 1)
head_subplot.set_title('Heading (deg)', y = 1)

plt.subplots_adjust(hspace = 0.7)
# pres_subplot.subplots_adjust(hspace = 1)
# head_subplot.subplots_adjust(hspace = 1)

tmpr_subplot.set_xlabel('time (s)')
pres_subplot.set_xlabel('time (s)')
head_subplot.set_xlabel('time (s)')

t_line, = tmpr_subplot.plot(0, 0, color = "blue")

p_line, = pres_subplot.plot(0, 0, color = "red")

h_line, = head_subplot.plot(0, 0, color = "black")


max_length = 10


def update_data(field, data):
	global tmpr, pres, head

	if field == "TMPR":
		tmpr = data

	elif field == "PRES":
		pres = data

	elif field == "HEAD":
		head = data





def plot(interval):
	global time_prev, tmpr_prev, pres_prev, head_prev


	time = (datetime.now() - starttime).total_seconds()
	

	time_list = [time_prev, time]
	tmpr_list = [tmpr_prev, tmpr]
	pres_list = [pres_prev, pres]
	head_list = [head_prev, head]


	tmpr_subplot.plot(time_list, tmpr_list, color = "blue")
	pres_subplot.plot(time_list, pres_list, color = "red")
	head_subplot.plot(time_list, head_list, color = "black")


	time_prev = time
	tmpr_prev = tmpr
	pres_prev = pres
	head_prev = head

	if(round(time) % refresh_rate == 0):
		cleargraphs()



def cleargraphs():
	tmpr_subplot.cla()
	pres_subplot.cla()
	head_subplot.cla()


def animate(interval):
	return animation.FuncAnimation(figure, plot, interval=interval)


def figure_canvas(figure, parent):
	return FigureCanvasTkAgg(figure, parent)


