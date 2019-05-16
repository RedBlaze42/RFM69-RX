import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

class email_handler():
	def __init__(self):
		self.addr="rednet.notifier@gmail.com"
		self.server = smtplib.SMTP('smtp.gmail.com', 587) 
		self.server.starttls() 
		self.server.login(self.addr, "rednet_notifier42") 
	
	def __del__(self):
		self.server.quit()

	def send_mail(self,to_addr,subject,body,file_list):
		msg = MIMEMultipart()
		msg["From"]=self.addr
		msg["To"]=to_addr
		msg["Subject"]=subject
		msg.attach(MIMEText(body, 'plain'))    
		for path,name in file_list:
			msg.attach(self.attach_file(path,name))
		self.server.sendmail(self.addr, to_addr, msg.as_string()) 

	def attach_file(self,path,name):
		attachment_file=open(path,"rb")
		payload = MIMEBase('application', 'octet-stream') 
		payload.set_payload((attachment_file).read()) 
		encoders.encode_base64(payload) 
		payload.add_header('Content-Disposition', "attachment; filename= "+name) 
		return payload