'''
import datetime

print("Print Todays Date and Time", datetime.datetime.now())
print("Print Todays Date", datetime.datetime.today())
print("Print only date", datetime.date(2025,10,10))
print("Print only time", datetime.time(10,10))
print("print create cutome date and time", datetime.datetime(2025,10,10,10,10))
print("Print only todays date", datetime.datetime.now().date())
print("Print only todays date", datetime.datetime.now().time())
print("Print only todays Hour", datetime.datetime.now().hour)
print("Print only todays Minute", datetime.datetime.now().minute)

now=datetime.datetime.now()
print("Now",now)
formated_now=now.strftime("%d:%m:%Y")
print(formated_now)

today=datetime.datetime.today()
print("Todays Date",today)
tomorrow=today - datetime.timedelta(days=365)
print("tomorrow date",tomorrow)

'''

from datetime import datetime
file_name="app.log"
now=datetime.now()
print(now)
timestamp=now.strftime("%Y-%m-%d")

log_message = f"{timestamp} - Application Started\n"

import os
file_path=os.path.join(os.getcwd(),"log",file_name)
with open(file_path,"a") as file:
    file.write(log_message)