#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial
import time
import os
import sys
import struct

from tkinter import Tk, Text, W, E, N, S, LEFT, RIGHT, BOTH, HORIZONTAL, Scale
from tkinter.ttk import Frame, Button, Style
from tkinter.colorchooser import *

clear = lambda: os.system('cls')
arduino = serial.Serial('COM3', 9600)

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
		def fire():
			arduino.write(struct.pack('>BBBB', 2,0,0,0))
			time.sleep(.1)
			arduino.write(struct.pack('>BBBB', 2,3,0,0))
			time.sleep(.1)
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

		arduino.write(struct.pack('>BBBB', 9,1,0,0))
		got = arduino.readline()[:-2].decode('utf-8').split()
		pal = got[0]
		bright = got[1]
		speed = got[2]
		direction = got[3]
		print(pal)
		print(bright)
		print(speed)
		print(direction)
		time.sleep(.1)
		arduino.flush()

		self.master.title("LED Meister")

		self.columnconfigure(0, pad=3)
		self.columnconfigure(1, pad=3)
		self.columnconfigure(2, pad=3)
		self.columnconfigure(3, pad=3)

		self.rowconfigure(0, pad=3)
		self.rowconfigure(1, pad=3)
		self.rowconfigure(2, pad=3)
		self.rowconfigure(3, pad=3)

		rbbutton = Button(self, text="Rainbow", command=rainbow)
		rbbutton.grid(row=1, column=0)

		bwbutton = Button(self, text="B&W", command=baw)
		bwbutton.grid(row=1, column=1)

		firebutton = Button(self, text="Fire", command=fire)
		firebutton.grid(row=1, column=2)

		lavabutton = Button(self, text="Lava", command=lava)
		lavabutton.grid(row=1, column=3)

		forbutton = Button(self, text="Forest", command=forest)
		forbutton.grid(row=2, column=0)

		oceanbutton = Button(self, text="Ocean", command=ocean)
		oceanbutton.grid(row=2, column=1)

		polbutton = Button(self,text="Police", command=police)
		polbutton.grid(row=2, column=2)

		parbutton = Button(self,text="Party", command=party)
		parbutton.grid(row=2, column=3)

		colbutton = Button(self, text="Solid color", command=customColor)
		colbutton.grid(row=3, column=0)

		brightslider = Scale(self, from_=0, to=127, orient=HORIZONTAL, label="Brightness", showvalue=0, sliderlength=20, length=230, width=10)
		brightslider.set(bright)
		brightslider.grid(row=4, column=0, columnspan=3)

		setbrightness = Button(self,text="Set", command=setbright)
		setbrightness.grid(row=4, column=3)

		speedslider = Scale(self, from_=25, to=255, orient=HORIZONTAL, label="Speed", showvalue=0, sliderlength=20, length=230, width=10)
		speedslider.set(speed)
		speedslider.grid(row=5, column=0, columnspan=3)

		setspeedbut = Button(self,text="Set", command=setspeed)
		setspeedbut.grid(row=5, column=3)

		invertbutton = Button(self, text="Invert rot.", command=invertrotation)
		invertbutton.grid(row=6, column=0)

		savebutton = Button(self, text="Save settings", command=savesettings)
		savebutton.grid(row=7, column=2)

		quitbutton = Button(self, text="Quit", command=self.quit)
		quitbutton.grid(row=7, column=3)

		self.pack()

def main():
	root = Tk()
	app = LEDMeister()
	root.mainloop()

if __name__ == '__main__':
	main()