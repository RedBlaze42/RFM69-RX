from errors import *
import standard_methods
import os
import importlib

class config:
	def find_lines(self,name):
		output=list()
		for line in self.data:
			line=line.split("|")
			if(line[0]==name):
				output.append("|".join(line[1:]))
		if len(output)==0:
			raise MissingConfig("Missing "+name+" parameter in conf file",name)
		else:
			return output
	
	def find_flag(self,name):
		output=list()
		for line in self.data:
			line=line.split("|")
			if(line[0]==name):
				return True
		return False
	def find_line(self,name):
		return self.find_lines(name)[0]

	def get_data_method_from_name(self,name):
		if(hasattr(self.methods, name)):
			return getattr(self.methods, name)
		elif(name.find("pass")!=-1):
			return standard_methods.pass_through_column(int(name.split("pass")[1]))
		else:
			raise MissingGraphMethod("Missing "+name+" method in methods file",name)

	def __init__(self,name="config.txt",usb_methods=False):
		if not os.path.exists(name):
			raise MissingConfigFile("Missing config file: "+name)
		if usb_methods:
			self.methods=importlib.import_module("usb_methods")
			if not os.path.exists("usb_methods.py"):
				raise MissingMethodFile("Missing method file")
		else:
			self.methods=importlib.import_module("default_processing_methods")
		self.config_file=open(name,"r")
		self.data=self.config_file.read().split("\n")
		
		self.graphs=self.find_lines("GRAPH")
		
		self.packet_number=int(self.find_line("PACKET_NUMBER"))
		self.max_flight_time=int(self.find_line("MAX_FLIGHT_TIME"))
		self.png=self.find_flag("NO_PNG")==False
		self.screen_data=self.find_flag("SCREEN_DATA")
		self.screen_data_name=self.find_line("SCREEN_DATA_NAME")
		if self.screen_data==False:#No screen data desired
			self.screen_data_column=None
			self.screen_data_method=None
		else:
			self.screen_data_column=int(self.find_line("SCREEN_DATA_COLUMN"))
			screen_data_method_name=self.find_line("SCREEN_DATA_METHOD")
			if(hasattr(self.methods, screen_data_method_name)):
				self.screen_data_method=getattr(self.methods,screen_data_method_name)
			else:
				self.screen_data_method=standard_methods.pass_through
		
		trigger_method_name=self.find_line("TRIGGER_METHOD")
		if(hasattr(self.methods, trigger_method_name)):
			self.trigger_method=getattr(self.methods,trigger_method_name)
		else:
			self.trigger_method=standard_methods.trigger_all

		self.png=self.find_flag("NO_PNG")==False
		self.email=self.find_flag("EMAIL")
		if self.email:
			self.email_adresses=self.find_lines("EMAIL_ADRESS")
		else:
			self.email_adresses=None