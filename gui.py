# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 15:04:38 2021
@author: npx.msc
"""

import serial
import tkinter as tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
'''
s = serial.Serial()
s.port = 'COM2'
s.timeout = 2
s.baudrate = 9600
s.open()
s.write(b'1')
s.readline()
'''
state = {'potency': [0,0,0,0,0],'temperature': [0,0,0,0,0]}

led1 = False
led2 = False
led3 = False

s = serial.Serial('COM2', 9600, timeout=2)


fig_pot = Figure(figsize = (3, 3), dpi = 90)
fig_temp = Figure(figsize = (3, 3), dpi = 90)
fig_pot.add_axes([0,8,10,50])
fig_temp.add_axes([0,0,10,50])


def create_window():
	main_window = tk.Tk()
	main_window.title("Final Project")

	topFrame = tk.Frame(main_window, bg='black', pady = 20)
	bottomFrame = tk.Frame(main_window, bg='white', pady = 20)

	main_window.geometry("750x550+50+50")
	return main_window,topFrame,bottomFrame

def swap_bool(controller):
	return not controller

def get_temperature():
	if not s.is_open: s.open()
	s.write(b'7')
	value = float(str(s.readline())[2:-1])
	s.close()
	return value

def get_potency():
	if not s.is_open: s.open()
	s.write(b'8')
	value = int(str(s.readline())[2:-1])
	s.close()
	return value

def get_data():
	if not s.is_open: s.open()
	s.write(b'9')
	data = str(s.readline()).split()
	s.close()
	potency = int(data[0][2::])
	temperature = float(data[1][0:-1])
	return potency, temperature

def onOff1():
	global led1
	global btn1
	if not s.is_open: s.open()
	s.write(b'1')
	s.close()
	btn1['text'] = 'On Led1' if led1 else 'Off Led1' 
	led1 = swap_bool(led1)

def onOff2():
	global led2
	global btn2
	if not s.is_open: s.open()
	s.write(b'2')
	s.close()
	btn2['text'] = 'On Led2' if led2 else 'Off Led2' 
	led2 = swap_bool(led2)

def onOff3():
	global led3
	global btn3
	if not s.is_open: s.open()
	s.write(b'3')
	s.close()
	btn3['text'] = 'On Led3' if led3 else 'Off Led3' 
	led3 = swap_bool(led3)

def left():
	if not s.is_open: s.open()
	s.write(b'4')
	s.close()

def right():
	if not s.is_open: s.open()
	s.write(b'5')
	s.close()

def offMotor():
	if not s.is_open: s.open()
	s.write(b'6')
	s.close()


def plot_potency():
	global state
	global fig_pot
	global potency_grah
	plot1 = fig_pot.add_subplot(111)
	plot1.plot(state['potency'],color='g',marker='o')
	potency_grah.draw()
	
	
def plot_temperature():
	global state
	global fig_temp
	global temperature_graph
	plot2 = fig_temp.add_subplot(111)
	
	
	plot2.plot(state['temperature'],color='b',marker='*')
	temperature_graph.draw()
	

def refreshSystem():
	global state
	global fig_pot
	global fig_temp
	global temperature_graph
	global potency_grah
	
	potency, temperature = get_data()
	
	state['potency'].append(potency)
	del(state['potency'][0])
	state['temperature'].append(temperature)
	del(state['temperature'][0])

	fig_pot.clf()
	fig_temp.clf()
	
	plot_potency()
	plot_temperature()
	
	main_window.after(1000, refreshSystem)	

main_window, top, bot = create_window()

btn1 = tk.Button(top, text = "On Led1",command = lambda: onOff1())
btn2 = tk.Button(top, text = "On Led2",command = lambda: onOff2())
btn3 = tk.Button(top, text = "On Led3",command = lambda: onOff3())
btn4 = tk.Button(top, text = "Left Motor",command = lambda: left())
btn5 = tk.Button(top, text = "Right Motor",command = lambda: right())
btn6 = tk.Button(top, text = "Off Motor",command = lambda: offMotor())


potency_grah = FigureCanvasTkAgg(fig_pot,master = bot)  
temperature_graph = FigureCanvasTkAgg(fig_temp,master = bot)  

potency_grah.get_tk_widget().grid(row = 0,column = 0, padx = 5, pady = 10)
temperature_graph.get_tk_widget().grid(row = 0,column = 1, padx = 5, pady = 10)

btn1.grid(row = 0,column = 0, padx = 10, pady = 10)
btn2.grid(row = 0,column = 1, padx = 10, pady = 10)
btn3.grid(row = 0,column = 2, padx = 10, pady = 10)
btn4.grid(row = 0,column = 3, padx = 10, pady = 10)
btn5.grid(row = 0,column = 4, padx = 10, pady = 10)
btn6.grid(row = 0,column = 5, padx = 10, pady = 10)

top.grid_columnconfigure(0,weight=1)
top.grid_columnconfigure(1,weight=1)
top.grid_columnconfigure(2,weight=1)
top.grid_columnconfigure(3,weight=1)
top.grid_columnconfigure(4,weight=1)
top.grid_columnconfigure(5,weight=1)

bot.grid_columnconfigure(0,weight=1)
bot.grid_columnconfigure(1,weight=1)



top.pack(fill='x')
bot.pack(fill='x')

refreshSystem()
s.close()
main_window.mainloop()

plt.close()

