import smtplib
import os 
import pytz
from datetime import datetime 

if __name__ == '__main__':
    tz_NY = pytz.timezone('Asia/Kolkata') 
    datetime_NY = datetime.now(tz_NY)
    time_=datetime_NY.strftime("%H:%M:%S")
    print(time_)
    sender = 'mdkenta09@gmail.com'
    receiver = 'mdkenta09@gmail.com'

    message = "hello"

    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receiver, message)         
    print("Successfully sent email")