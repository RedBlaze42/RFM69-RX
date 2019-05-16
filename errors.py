from datetime import datetime

class MissingConfig(Exception):
	def __init__(self,message,config_missing):
		super().__init__(message)

		with open("log.txt","a") as log:
			log.write("["+datetime.now().strftime("%d/%m/%Y, %H:%M:%S")+"]ERROR MissingConfig: "+message)

class MissingGraphMethod(Exception):
	def __init__(self,message,method_missing):
		super().__init__(message)
		
		with open("log.txt","a") as log:
			log.write("["+datetime.now().strftime("%d/%m/%Y, %H:%M:%S")+"]ERROR MissingGraphMethod: "+message+"\n")

class MissingConfigFile(Exception):
	def __init__(self,message):
		super().__init__(message)
		
		with open("log.txt","a") as log:
			log.write("["+datetime.now().strftime("%d/%m/%Y, %H:%M:%S")+"]ERROR MissingConfigFile: "+message+"\n")

class MissingMethodFile(Exception):
	def __init__(self,message):
		super().__init__(message)
		
		with open("log.txt","a") as log:
			log.write("["+datetime.now().strftime("%d/%m/%Y, %H:%M:%S")+"]ERROR MissingMethodFile\n")