#This code has no guarantees of correctness or security.

import sys
import urllib.request
import smtplib
from email.mime.text import MIMEText
import time

GMAIL_USERNAME = 'bjjhqscript@gmail.com' #change this to the email to send from. Make sure to enable less secure applications for the account from here https://www.google.com/settings/security/lesssecureapps 
GMAIL_PASSWORD = 'test' #the password to the account above
email_subject = 'MySubj'
recipient = 'temp@temp.com' #the email address to send the notification to. You don't need to enable less secure applications for this one. It can be the same as above if you want.
body_of_email = 'this is the email.......'


localtime = time.asctime( time.localtime(time.time()) )
print("Time on startup : ", localtime )
print("Sleeping for 20 minutes")
#time.sleep(1200) #sleep for 20 minutes
localtime = time.asctime( time.localtime(time.time()) )
print("Time on wakeup : ", localtime )

while(1 == 1) :

	
	try:
		response = urllib.request.urlopen('http://www.bjjhq.com/')
	except urllib.error.HTTPError as err:
		localtime = time.asctime( time.localtime(time.time()) )
		print("Error caught at: ", localtime )
		print(err.code)
		time.sleep(10)
		continue
	#except:
	#	localtime = time.asctime( time.localtime(time.time()) )
	#	print("Unexpected Error at: ", localtime )
	#	raise
		
	html = response.read()
	txt = str( html, encoding='cp437' )
	lines = txt.split('\n')
	found = 0
	for l in lines :
		if (l.find("<h1>") != -1):
			item_title  = l.lstrip()
			if( (l.find("Fuji") != -1) or (l.find("Inverted") != -1) ):  #these are the keywords to look for. I believe they are case sensitive so be careful. You can modify this "if" statement to add more or less.
				body_of_email = l.lstrip()
				email_subject = l.lstrip()
				# The below code never changes, though obviously those variables need values.
				session = smtplib.SMTP('smtp.gmail.com', 587)
				session.ehlo()
				session.starttls()
				session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
				headers = "\r\n".join(["from: " + GMAIL_USERNAME,
							   "subject: " + email_subject,
							   "to: " + recipient,
							   "mime-version: 1.0",
							   "content-type: text/html"])

				# body_of_email can be plaintext or html!                    
				content = headers + "\r\n\r\n" + body_of_email
				session.sendmail(GMAIL_USERNAME, recipient, content)
				
				print("Sending email for item: ", l.lstrip() )
				found = 1
				break

	if(found == 0):
		print("Not found in line: " , item_title )

	time.sleep(60) # delays for 30 seconds then looks again. It will send another email if the item is still a match.

