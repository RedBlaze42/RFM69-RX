import board
import busio
import digitalio
import time
import os
import adafruit_rfm69
import errors
import email_handler

from outils import *
import config as config_handler
from plotter import plotter
import lcd_handler

reception=True
shutdown=False
usb_timeout=10

lcd=lcd_handler.lcd()
#CONFIG SETUP
os.system("sudo umount /dev/sda1")
os.system("mkdir -p usb")
os.system("rm usb_methods.py")

if ((os.system("sudo mount -o umask=002,gid=1000,uid=1000 /dev/sda1 usb")==0 or check_mount("usb")) and os.path.exists("usb/FLIGHT_DATA/config.txt")):
	lcd.prompt("SETUP","USB CONFIG")
	time.sleep(3)
	if(os.path.exists("usb/FLIGHT_DATA/methods.py")):
		os.system("cp usb/FLIGHT_DATA/methods.py usb_methods.py")
		usb_methods_copied=True
		lcd.prompt("SETUP","USB METHODS")
	else:
		usb_methods_copied=False
		lcd.prompt("SETUP","DEFAULT METHODS")
	config=config_handler.config(name="usb/FLIGHT_DATA/config.txt",usb_methods=usb_methods_copied)
	os.system("sudo umount /dev/sda1")
	time.sleep(3)
else:
	config=config_handler.config()
	lcd.prompt("SETUP","DEFAULT CONFIG")
	time.sleep(2)
	lcd.prompt("SETUP","DEFAULT METHODS")
	time.sleep(2)


##SETUP
CS = digitalio.DigitalInOut(board.D7)
RESET = digitalio.DigitalInOut(board.D5)
spibus = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rf = adafruit_rfm69.RFM69(spibus, CS, RESET, 433.0)
rf.encryption_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'

#DATA SETUP
os.system("mkdir -p DATA")

i=0
while os.path.exists("DATA/"+str(i)+"/"):
	i+=1
data_number=1

data_path="DATA/"+str(data_number)+"/"
graphs_pdf_path=data_path+"GRAPHS/"
graphs_png_path=graphs_pdf_path+"pictures/"
os.system("mkdir -p "+data_path+" "+graphs_pdf_path+" "+graphs_png_path)
data=open(data_path+"DATA.txt","a")

if reception:
	##RECEPTION
	lcd.prompt("BEGIN RECEPTION")
	time.sleep(2)
	lcd.prompt("LP=time since","last packet")
	time.sleep(3)
	lcd.prompt("TO=time to end","of the flight")
	time.sleep(3)
	
	packet_index=0
	packet_buffer=list()
	start_time=time.time()
	lcd.recieve_timeout=start_time+config.max_flight_time#To print remaining time
	lcd.data_name=config.screen_data_name
	
	while ((time.time()-start_time)<config.max_flight_time):
		packet = rf.receive(timeout=1)
		if packet==None:
			lcd.recieve_packets()
			continue

		packet=str(packet, 'ascii')
		if(packet=="END"):#End condition
			break
		else:
			packet=packet.split("|")

		if(int(packet[0])==packet_index):
			packet_buffer.extend(packet[1:])
			packet_index+=1

		if(packet_index>=config.packet_number):
			data.writelines("|".join(packet_buffer)+"\n")

			lcd.time_last_packet=time.time()
			if config.screen_data:
				lcd.data=config.screen_data_method(packet_buffer[config.screen_data_column])

			packet_buffer=list()
			packet_index=0
		lcd.recieve_packets()
	data.close()
	lcd.prompt("END OF FLIGHT")
	time.sleep(5)

##GRAPHS
lcd.prompt("GRAPH GENERATION","Data formatting")
with open(data_path+"DATA.txt","r") as data_file:
	data=data_file.read().split("\n")

#DATA FORMAT TO COLUMNS FOR TRIGGER DETECTION
columns_number=len(data[0].split("|"))
columns=list()
for i in range(columns_number):#CREATE COLUMN LIST
	columns.append(list())
for line in data:
	line=line.split("|")
	for i in range(columns_number):
		columns[i].append(float(line[i]))#Append data

#TRIGGER DETECTION
trigger_line,end_trigger_line,time_offset=config.trigger_method(columns)#return linestart,lineend,time_offset

#CROP BY TRIGGER, TIME OFFSETTING AND FORMAT
columns_number=len(data[0].split("|"))
columns=list()
for i in range(columns_number):#CREATE COLUMN LIST
	columns.append(list())
for line in data:
	line=line.split("|")
	for i in range(columns_number):
		if(i==0):#If column number==0 (time column)
			columns[i].append(float(line[i])-time_offset)#Append updated time
		else:
			columns[i].append(float(line[i]))#Append other data

del data#FREE RAM

#GRAPH CREATION
pdf_file_list,png_file_list=list(),list()
graph_parameters_index={"title":0,"x_legend":1,"y_legend":2,"x_unit":3,"y_unit":4,"x_method":5,"y_method":6,"annotate":7}
ending_commands=list()
lcd.prompt("GRAPH GENERATION","0/"+str(len(config.graphs)))
for graph_number,graph in enumerate(config.graphs):
	graph_parameters_list=graph.split("|")
	graph_parameters=dict()
	for parameter in graph_parameters_index.items():#Set graph parameter list in a named dict
		graph_parameters[parameter[0]]=graph_parameters_list[parameter[1]]

	x=config.get_data_method_from_name(graph_parameters["x_method"])(columns)
	y=config.get_data_method_from_name(graph_parameters["y_method"])(columns)

	annotate=True if graph_parameters["annotate"]==1 else False
	
	plotter(x,y,
		graphs_pdf_path+graph_parameters["title"]+".pdf",#pdf file path
		graph_parameters["x_legend"],graph_parameters["y_legend"],
		graph_parameters["title"],
		graph_parameters["x_unit"],graph_parameters["y_unit"],
		annotate)

	png_file_list.append("\""+graphs_png_path+graph_parameters["title"]+".png"+"\"")
	pdf_file_list.append("\""+graphs_pdf_path+graph_parameters["title"]+".pdf"+"\"")
	ending_commands.append("convert -density 250 "+"\""+graphs_pdf_path+graph_parameters["title"]+".pdf"+"\""+" -quality 90 \""+graphs_png_path+graph_parameters["title"]+".png\"")

	lcd.prompt("GRAPH GENERATION",str(graph_number+1)+"/"+str(len(config.graphs)))

#GRAPH CONVERSION
if config.png:
	lcd.prompt("GRAPH GENERATION","Finalising "+"0/"+str(len(ending_commands)+1))
	os.system("gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/default -dNOPAUSE -dQUIET -dBATCH -dDetectDuplicateImages -dCompressFonts=true -r150 -sOutputFile="+graphs_pdf_path+"all_graphs.pdf"+" "+" ".join(pdf_file_list))
	for i,command in enumerate(ending_commands):
		lcd.prompt("GRAPH GENERATION","Finalising "+str(i+1)+"/"+str(len(ending_commands)+1))
		os.system(command)

lcd.prompt("GRAPH GENERATION","SUCCESS")
time.sleep(5)

#COPY TO USB
lcd.prompt("COPYING","INSERT USB STICK")
time.sleep(1)
os.system("mkdir -p usb")
os.system("sudo umount /dev/sda1")
start_mounting_time=time.time()
while ((os.system("sudo mount -o umask=002,gid=1000,uid=1000 /dev/sda1 usb")!=0) and check_mount("usb")==False) and (time.time()-start_mounting_time<usb_timeout):
	time.sleep(1)
	lcd.prompt("COPYING","INSERT USB "+lcd.format_number(usb_timeout-(time.time()-start_mounting_time),2))
if check_mount("usb"):
	lcd.prompt("COPYING","USB OK")
	os.system("cp -R DATA usb/")
	os.system("rm -R LAST_LAUNCH")
	os.system("mkdir -p usb/LAST_LAUNCH")
	os.system("cp -R DATA/"+str(data_number)+"/* usb/LAST_LAUNCH/")
else:
	lcd.prompt("COPYING","NO USB")
	time.sleep(5)

#EMAIL
if config.email and check_insternet_connection():
	lcd.prompt("MAIL","SENDING")
	if config.png:#Check which type of file has to be sent
		file_list=png_file_list
	else:
		file_list=pdf_file_list
	attachment_list=list()
	for file_path in file_list:#Get filename and filepath
		file_path=file_path.replace("\"","")
		if os.path.exists(file_path):
			file_name=file_path.split("/")[-1]
			attachment_list.append( (file_path,file_name) )
		attachment_list.append( (graphs_pdf_path+"all_graphs.pdf","all_graphs.pdf") )

	for adress in config.email_adresses:
		email=email_handler.email_handler()
		email.send_mail(adress,"FLIGHT DATA","Here is the early processed flight data",attachment_list)
	
	lcd.prompt("MAIL","SENT")
	time.sleep(5)
lcd.prompt("END","SHUTDOWN")
time.sleep(5)
if shutdown: os.system("sudo shutdown now")