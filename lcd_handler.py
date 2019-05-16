from RPLCD import CharLCD
from RPi import GPIO
from outils import *
from time import time

class lcd:
	
	def __init__(self,cols=16,rows=2):
		self.cols,self.rows= cols,rows
		self.blink=False
		self.data=None
		self.data_name=None
		self.time_last_packet=0
		self.recieve_timeout=None
		GPIO.setmode(GPIO.BCM)
		self.screen = CharLCD(numbering_mode=GPIO.BCM,cols=self.cols, rows=self.rows, pin_rs=16, pin_e=18, pins_data=[23, 24, 2, 3])
	
	def prompt(self,text,text2=""):
		self.screen.clear()
		self.write(text)
		self.screen.cursor_pos = (1,0)
		self.write(text2)
	def write(self,text):
		print(self.screen.cursor_pos,text)
		self.screen.write_string(text[:self.cols])
		
	
	def format_number(self,number,digits):
		output=digit(number,digits)
		if len(output)>digits:
			output="9"
			while(len(output)<digits):
				output+="9"
		return output
	
	def recieve_packets(self):
		self.screen.clear()

		self.write("R LP:"+self.format_number(time()-self.time_last_packet,2)+"s")
		if(self.recieve_timeout!=None):
			remaining_time=self.recieve_timeout-time()
			self.cursor_pos=(0,9)
			self.write("TO:"+self.format_number(remaining_time,3)+"s")
		
		if self.data_name!=None and self.data!=None:
			self.screen.cursor_pos = (1,0)
			self.write(self.data_name+": ")
			data_digits=self.cols-len(self.data_name)
			data=self.format_number(self.data,data_digits)
			self.screen.cursor_pos = (1,self.cols-data_digits)
			self.write(data)
		if self.blink:
			self.screen.cursor_pos = (0,1)
			self.write(".")
			self.blink=False
		else:
			self.blink=True