'''from email.message import EmailMessage
import smtplib
def mail_sender(email_to,subject,body):
        Email_Address='anurupa070@gmail.com'
        Email_Password='kxsfvxbysyiyhlyp'
        msg=EmailMessage()
        msg['Subject']='hi'
        msg['From']=Email_Address
        msg['To']='206841@siddharthamahila.ac.in'
        #msg.set_content(body)
        smtp1=smtplib.SMTP_SSL('smtp.gmail.com',465)
        smtp1.login(Email_Address,Email_Password)
        smtp1.send_message(msg)
        smtp1.quit()'''

 

from email.message import EmailMessage
import smtplib
def mail_sender(email,email_to,subject,passcode,body):
        Email_Address='anurupa070@gmail.com'
        Email_Password='kxsfvxbysyiyhlyp'
        msg=EmailMessage()
        msg['Subject']=subject
        msg['From']=Email_Address
        msg['To']=email_to
        msg.set_content(body)
        smtp1=smtplib.SMTP_SSL('smtp.gmail.com',465)
        smtp1.login(Email_Address,Email_Password)
        smtp1.send_message(msg)
        smtp1.quit()

