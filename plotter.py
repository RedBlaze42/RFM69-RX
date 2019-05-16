import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib

def indexMax(index,values):
	maxValue,maxIndex=0,0
	
	for i in range(len(values)):
		if(values[i]>=maxValue):
			maxValue,maxIndex=values[i],index[i]
	return maxIndex,maxValue

def indexMin(index,values):
	minValue,minIndex=indexMax(index,values)[1],0
	
	for i in range(len(values)):
		if(values[i]<=minValue):
			minValue,minIndex=values[i],index[i]
	return minIndex,minValue

def plotter(x,y,path,x_text,y_text,title,x_unit,y_unit,annotate=True):
	fig, ax = plt.subplots()
	
	plt.plot(x, y, linestyle='solid', ms=1)
	plt.xlabel(x_text)
	plt.ylabel(y_text)
	plt.title(title)
	maxDATA=indexMax(x,y)#index of maximum, value of maximum
	minDATA=indexMin(x,y)#index of minimum, value of minimum
	if annotate:
		plt.annotate('Max: '+str(maxDATA[1])+y_unit+"\n"+maxDATA[0].strftime(str_format),maxDATA,xytext=(5,-30),textcoords='offset pixels',annotation_clip=True)
		plt.annotate('Min: '+str(minDATA[1])+y_unit+"\n"+minDATA[0].strftime(str_format),minDATA,xytext=(5,-30),textcoords='offset pixels',annotation_clip=True)
	ax.grid(True)
	
	plt.savefig(path,bbox_inches='tight')
	plt.clf()