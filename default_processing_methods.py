#TRIGGER input: (data) list of columns | output: trigger_index_start,trigger_index_end,time_offset
#SCREEN DATA: (data) input list of values | output: integer
#GRAPH input: (data) list of columns | output: list of values

def trigger_altitude(data):
	altitude_offset=data[1][10]

	trigger_index_start=0#Start
	for i,altitude in enumerate(data[1]):#Check index when altitude>10m
		if(altitude-altitude_offset>=10):
			trigger_index_start=i
			break
	time_offset=data[0][trigger_index_start]-10#Get the time 10sec before launch
	for i,time in enumerate(data[0]):#Get the index 10sec before launch
		if(time>=time_offset):
			trigger_index_start=i
			break

	trigger_index_end=0#End
	for i,altitude in enumerate(data[1]):
		if(altitude-altitude_offset<=10) and (i>trigger_index_start+10):#Get the index when altitude<10 but after launch
			trigger_index_end=i
			break
		else:
			trigger_index_end=len(data[0])#Last index if no landing
	trigger_time_end=data[0][trigger_index_end]+10#Get the time 10secs after landing
	for i,time in enumerate(data[0]):#Get the index 10secs after landing
		if(time>=trigger_time_end):
			trigger_index_end=i
			break
		else:
			trigger_index_end=len(data[0])#Last index if no landing

	return trigger_index_start,trigger_index_end,time_offset