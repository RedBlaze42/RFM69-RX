import os
import socket

def digit(input,nb):
	output=str(int(input))
	while(len(output)<nb):
		output="0"+output
	return output

def check_mount(mountpoint):
	mount_file=open("/proc/mounts",'r')
	data=mount_file.read().split("\n")
	mount_file.close()
	for line in data:
		if(line.find(mountpoint)!=-1):
			return True
	return False


def check_insternet_connection(hostname="www.google.com"):
	try:
		host = socket.gethostbyname(hostname)
		s = socket.create_connection((host, 80), 2)
		return True
	except:
		pass
	return False