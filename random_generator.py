from math import *
import random
line_number=10000

data=list()
for i in range(1,line_number):
	trame=[i,sin(i)*10,i/line_number, random.randint(0,i), random.randint(int(i/2),i), random.randint(i,line_number)]
	for i,value in enumerate(trame):
		trame[i]=str(value)
	data.append("|".join(trame))

with open("DATA.txt","w") as data_file:
	data_file.write("\n".join(data))