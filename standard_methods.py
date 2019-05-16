#TRIGGER input: (data) list of columns | output: trigger_index_start,trigger_index_end,time_offset
#SCREEN DATA: (data) input list of values | output: integer
#GRAPH input: (data) list of columns | output: list of values

#################################################################
def pass_through_column(column):
	def pass_through(data):#data=column list
		output=list()
		for value in data[column]:
			output.append(float(value))
		return output
	return pass_through

def pass_through(data):
	return data

def trigger_all(data):
	return 0,len(data[0]),0#Start index, end index, time offset
#################################################################