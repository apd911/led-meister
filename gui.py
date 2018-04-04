#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial
import time
import os
import sys
import struct
import serial.tools.list_ports

from tkinter import Tk, Text, W, E, N, S, LEFT, RIGHT, BOTH, HORIZONTAL, Scale, Menu, Label
from tkinter.ttk import Frame, Button, Style
from tkinter.colorchooser import *

fileR = open('settings.txt', 'r')

ports = list(serial.tools.list_ports.comports())
if fileR.readline(3) != 'COM':
	com = ports[0][0]
else:
	com = 'COM' + fileR.readline()

fileR.close()
arduino = serial.Serial(com, 9600)

clear = lambda: os.system('cls')

port = []

pal = "N/A"
bright = 0
speed = 20
time.sleep(2)
i = True
clear()

class LEDMeister(Frame):
	
	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):
		def rainbow():
			arduino.write(struct.pack('>BBBB', 2,1,0,0))
			time.sleep(.1)
			arduino.flush()
		def baw():
			arduino.write(struct.pack('>BBBB', 2,2,0,0))
			time.sleep(.1)
			arduino.flush()
		def fire1():
			arduino.write(struct.pack('>BBBB', 2,3,0,0))
			time.sleep(.1)
			arduino.flush()
		def fire2():
			arduino.write(struct.pack('>BBBB', 2,7,0,0))
			time.sleep(.1)
			arduino.flush()
		def lava():
			arduino.write(struct.pack('>BBBB', 2,5,0,0))
			time.sleep(.1)
			arduino.flush()
		def forest():
			arduino.write(struct.pack('>BBBB', 2,6,0,0))
			time.sleep(.1)
			arduino.flush()
		def ocean():
			arduino.write(struct.pack('>BBBB', 2,4,0,0))
			time.sleep(.1)
			arduino.flush()
		def police():
			arduino.write(struct.pack('>BBBB', 2,8,0,0))
			time.sleep(.1)
			arduino.flush()
		def party():
			arduino.write(struct.pack('>BBBB', 2,9,0,0))
			time.sleep(.1)
			arduino.flush()
		def turnoff():
			arduino.write(struct.pack('>BBBB', 2,0,0,0))
			time.sleep(.1)
			arduino.flush()
		def customColor():
			color = askcolor()
			if color:
				red = int(color[0][0])
				green = int(color[0][1])
				blue = int(color[0][2])
				colors = (4, red, green, blue)
				print(colors)
				arduino.write(struct.pack('>BBBB', 4,red,green,blue))
				time.sleep(.1)
				arduino.flush()
		def setbright():
			arduino.write(struct.pack('>BBBB', 1,2,brightslider.get(),0))
			time.sleep(.1)
			arduino.flush()
		def setspeed():
			arduino.write(struct.pack('>BBBB', 1,4,speedslider.get(),0))
			time.sleep(.1)
			arduino.flush()
		def savesettings():
			arduino.write(struct.pack('>BBBB', 3,0,0,0))
			time.sleep(.1)
			arduino.flush()
		def invertrotation():
			arduino.write(struct.pack('>BBBB', 1,3,0,0))
			time.sleep(.1)
			arduino.flush()
		def makeFunc(x):
			return lambda: self.openPort(x)

		active = True

		pal = 0
		bright = 0
		speed = 0

		arduino.write(struct.pack('>BBBB', 9,1,0,0))
		arduino.timeout = 5
		print(com)
		try:
			got = arduino.readline()[:-2].decode('utf-8').split()
			if got[4] == 'arduino':
				connected = True
				pal = got[0]
				bright = got[1]
				speed = got[2]
				print(pal)
				print(bright)
				print(speed)
				time.sleep(.1)
				if got[3] == '9':
					active = False;
			else:
				connected = False
				print('Not connected to an LED strip')
		except:
			connected = False
		
		arduino.flush()

		if connected == True:
			status = com + ' - ' + got[5]
		else:
			status = "Not connected to an LED strip"

		t = 0

		self.master.title("LED Meister")

		menubar = Menu(self.master)
		self.master.config(menu=menubar)

		fileMenu = Menu(menubar, tearoff=False)
		fileMenu.add_command(label="Save settings", command=savesettings)
		fileMenu.add_command(label="Save & exit", command=self.onSaveExit)
		fileMenu.add_command(label="Exit", command=self.onExit)
		menubar.add_cascade(label="File", menu=fileMenu)

		optionsMenu = Menu(menubar, tearoff=False)
		optionsMenu.add_command(label="Invert rotation", command=invertrotation)
		
		menubar.add_cascade(label="Options", menu=optionsMenu)
		if active == False:
			menubar.entryconfig('Options', state='disabled')

		portsMenu = Menu(menubar, tearoff=False)
		for p in ports:
			port.append(str(p[0]))
			portsMenu.add_command(label=p, command=makeFunc(port[t]))
			t = t + 1
		menubar.add_cascade(label="Ports", menu=portsMenu)

		self.columnconfigure(0, pad=3)
		self.columnconfigure(1, pad=3)
		self.columnconfigure(2, pad=3)
		self.columnconfigure(3, pad=3)

		self.rowconfigure(0, pad=3)
		self.rowconfigure(1, pad=3)
		self.rowconfigure(2, pad=3)
		self.rowconfigure(3, pad=3)

		rbbutton = Button(self, text="Rainbow", command=rainbow)
		if active == False:
			rbbutton['state'] = 'disabled'
		rbbutton.grid(row=1, column=0)

		bwbutton = Button(self, text="B&W", command=baw)
		if active == False:
			bwbutton['state'] = 'disabled'
		bwbutton.grid(row=1, column=1)

		firebutton = Button(self, text="Fire 1", command=fire1)
		if active == False:
			firebutton['state'] = 'disabled'
		firebutton.grid(row=1, column=2)

		fire2button = Button(self, text="Fire 2", command=fire2)
		if active == False:
			fire2button['state'] = 'disabled'
		fire2button.grid(row=1, column=3)

		lavabutton = Button(self, text="Lava", command=lava)
		if active == False:
			lavabutton['state'] = 'disabled'
		lavabutton.grid(row=2, column=0)

		oceanbutton = Button(self, text="Ocean", command=ocean)
		if active == False:
			oceanbutton['state'] = 'disabled'
		oceanbutton.grid(row=2, column=1)

		polbutton = Button(self,text="Police", command=police)
		if active == False:
			polbutton['state'] = 'disabled'
		polbutton.grid(row=2, column=2)

		forbutton = Button(self, text="Forest", command=forest)
		if active == False:
			forbutton['state'] = 'disabled'
		forbutton.grid(row=2, column=3)

		colbutton = Button(self,text="Party", command=party)
		if active == False:
			colbutton['state'] = 'disabled'
		colbutton.grid(row=3, column=0)

		parbutton = Button(self, text="Solid color", command=customColor)
		parbutton.grid(row=3, column=1)

		offbutton = Button(self, text="Turn off", command=turnoff)
		offbutton.grid(row=3, column=3)

		brightslider = Scale(self, from_=0, to=127, orient=HORIZONTAL, label="Brightness", showvalue=0, sliderlength=20, length=230, width=10)
		brightslider.set(bright)
		brightslider.grid(row=4, column=0, columnspan=3)

		setbrightness = Button(self,text="Set", command=setbright)
		setbrightness.grid(row=4, column=3)

		speedslider = Scale(self, from_=25, to=255, orient=HORIZONTAL, label="Speed", showvalue=0, sliderlength=20, length=230, width=10)
		speedslider.set(speed)
		speedslider.grid(row=5, column=0, columnspan=3)

		setspeedbut = Button(self, text="Set", command=setspeed)
		if active == False:
			setspeedbut['state'] = 'disabled'
		setspeedbut.grid(row=5, column=3)

		porttext = Label(self, text=status)
		porttext.grid(row=6, column=0, columnspan=4)

		self.pack()

	def openPort(self, portselected):
		fileW = open('settings.txt', 'w')
		fileW.write(portselected)
		fileW.close()
		os.execl(sys.executable, sys.executable, *sys.argv)

	def onSaveExit(self):
		arduino.write(struct.pack('>BBBB', 3,0,0,0))
		time.sleep(.1)
		arduino.flush()
		time.sleep(0.5)
		arduino.setDTR(False)
		time.sleep(0.022)
		arduino.setDTR(True)
		self.quit()


	def onExit(self):
		arduino.setDTR(False)
		time.sleep(0.022)
		arduino.setDTR(True)
		self.quit()

def main():
	def closeEvent():
		arduino.setDTR(False)
		time.sleep(0.022)
		arduino.setDTR(True)
		quit()
	root = Tk()
	app = LEDMeister()
	root.protocol("WM_DELETE_WINDOW", closeEvent)
	root.mainloop()

if __name__ == '__main__':
	main()