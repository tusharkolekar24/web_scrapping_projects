#!/usr/bin/env python
# coding: utf-8

# In[366]:


import yfinance as yf
import datetime
import matplotlib.pyplot as plt


# In[367]:


cochineship_stock= yf.Ticker("HAL.NS")
cochineship_historical = cochineship_stock.history(start="2021-01-01", end="2024-04-01", interval="1d")
cochineship_historical


# In[368]:


plt.figure(figsize=(20,8))
plt.subplot(3,1,1)
# plt.plot(cochineship_historical['Open'],label='Open')
plt.plot(cochineship_historical['Close'],label='Close')
# plt.plot(cochineship_historical['High'],label='High')
# plt.plot(cochineship_historical['Low'],label='Low')
plt.legend()

plt.subplot(3,1,2)
# plt.plot(cochineship_historical['Open'],label='Open')
plt.plot(cochineship_historical['Volume'],label='Volume')
plt.legend()

plt.subplot(3,1,3)
# plt.plot(cochineship_historical['Open'],label='Open')
plt.plot(cochineship_historical['Volume'].cumsum(),label='Volume')
plt.legend()
plt.show()


# In[369]:


cochineship_historical['Date'] = cochineship_historical.index


# In[370]:


cochineship_historical['Trade'] = cochineship_historical['Volume']/11810715


# In[371]:


cochineship_historical.corr()['Volume']


# In[372]:


cochineship_historical['Volume'].max()


# In[373]:


cochineship_historical['Volume'].max()-11810715


# In[374]:


import pandas as pd
import matplotlib.pyplot as plt


# In[375]:


cochineship_historical[cochineship_historical['Dividends']!=0]


# In[376]:


cochineship_historical[cochineship_historical['Stock Splits']!=0]


# In[377]:


cochineship_stock.dividends


# In[378]:


4623992>11810715


# In[379]:


len([f for f in cochineship_stock.info.keys()])


# In[380]:


cochineship_stock.info.get('companyOfficers')


# In[381]:


cochineship_stock.info


# In[382]:


import plotly.express as px

fig = px.line(cochineship_historical, x="Date", y="Volume", title='COCHINSHIP')
fig.update_layout(plot_bgcolor='white',)
fig.show()


# In[383]:


fig = px.line(cochineship_historical, x="Date", y="Close", title='COCHINSHIP')
fig.update_layout(plot_bgcolor='white',)
fig.show()


# In[384]:


import numpy as np
shift_dataset = cochineship_historical[['Close','Volume']].shift(1).reset_index()
shift_dataset.columns=['Date','Shift_Close','Shift_Volume']
cochineship_historical.index = np.arange(0,cochineship_historical.shape[0])


# In[385]:


shift_dataset


# In[386]:


1932698/4623992


# In[410]:


mergeset = pd.merge(cochineship_historical,shift_dataset,
         left_on=['Date'],
         right_on=['Date'],
         how='left')


# In[388]:


mergeset.drop(index=[0],inplace=True)


# In[411]:


mergeset['Denormalized_Price'] = mergeset['Close']-mergeset['Shift_Close']
mergeset['Denormalized_Vol'] = mergeset['Volume']-mergeset['Shift_Volume']


# In[412]:


mergeset['Year'] = mergeset['Date'].apply(lambda x:int(str(x).split("-")[0]))
#mergeset['Month_Day'] = mergeset['Date'].apply(lambda x:str(x).split("T")[0][5:].split(" ")[0])
mergeset['Month'] = mergeset['Date'].apply(lambda x:int(str(x).split("T")[0].split("-")[1]))


# In[413]:


month_map = {
  1: "January",
  2: "February",
  3: "March",
  4: "April",
  5: "May",
  6: "June",
  7: "July",
  8: "August",
  9: "September",
  10: "October",
  11: "November",
  12: "December"
}


# In[414]:


mergeset['Months'] = mergeset['Month'].map(month_map)


# In[415]:


# mergeset['Months'].values


# In[416]:


mergeset['Day'] = mergeset['Date'].apply(lambda x:int(str(x).split("T")[0].split("-")[2].split(" ")[0]))


# In[417]:


mergeset['Month_Day'] = ["{}_{}".format(i,j) for i,j in zip(mergeset['Months'],mergeset['Day'])]


# In[418]:


mergeset#[mergeset['Year']==2023]


# In[397]:


# history = mergeset.groupby(['Year','Month'])['Denormalized_Vol'].agg(['mean']).reset_index()
# history.rename(columns={"mean":"Denormalized_Price"},inplace=True)


# In[398]:


# mergeset['Year'] = mergeset['Year'].astype(str)


# In[399]:


# fig = px.scatter(mergeset, x="Date", y="Close", title='COCHINSHIP',color='Year')
# fig.update_layout(plot_bgcolor='white',)
# fig.show()


# In[419]:


upper_limit0 = mergeset["Denormalized_Vol"].mean()+3*mergeset["Denormalized_Vol"].std()
lower_limit0 = mergeset["Denormalized_Vol"].mean()-3*mergeset["Denormalized_Vol"].std()


# In[420]:


mergeset[mergeset['Year']==2024]["Denormalized_Vol"].max(),mergeset[mergeset['Year']==2024]["Denormalized_Vol"].min()


# In[421]:


mergeset[(mergeset['Year']==2024) & (mergeset['Denormalized_Vol']>=3820070.0)]#["Denormalized_Vol"].max()


# In[423]:


fig = px.line(mergeset, x="Date", y="Denormalized_Vol", title='COCHINSHIP',color='Year')
fig.add_hline(upper_limit0,line_width=2, line_dash="dash",line_color="green",
              annotation_text="Upper Limit", 
              annotation_position="top left")

fig.add_hline(lower_limit0,line_width=2, line_dash="dash",line_color="green",
              annotation_text="Lower Limit", 
              annotation_position="bottom left")
fig.update_layout(plot_bgcolor='white',)
fig.show()


# In[404]:


upper_limit = mergeset["Denormalized_Price"].mean()+8*mergeset["Denormalized_Price"].std()
lower_limit = mergeset["Denormalized_Price"].mean()-8*mergeset["Denormalized_Price"].std()

upper_limit1 = mergeset["Denormalized_Price"].mean()+6*mergeset["Denormalized_Price"].std()
lower_limit1 = mergeset["Denormalized_Price"].mean()-6*mergeset["Denormalized_Price"].std()

upper_limit2 = mergeset["Denormalized_Price"].mean()+4*mergeset["Denormalized_Price"].std()
lower_limit2 = mergeset["Denormalized_Price"].mean()-4*mergeset["Denormalized_Price"].std()

upper_limit3 = mergeset["Denormalized_Price"].mean()+2.5*mergeset["Denormalized_Price"].std()
lower_limit3 = mergeset["Denormalized_Price"].mean()-2.5*mergeset["Denormalized_Price"].std()


# In[405]:


upper_limit3


# In[406]:


fig = px.line(mergeset, x="Date", y="Denormalized_Price", title='COCHINSHIP',color='Year')
fig.add_hline(upper_limit,line_width=2, line_dash="dash",line_color="green",
              annotation_text="100%(Sell)", 
              annotation_position="top left")

fig.add_hline(upper_limit1,line_width=2, line_dash="dash",
              annotation_text="75%(Sell)",line_color="orange", 
              annotation_position="top left")

fig.add_hline(upper_limit2,line_width=2, line_dash="dash",
              annotation_text="50%(Sell)", line_color="pink", 
              annotation_position="top left")

fig.add_hline(upper_limit3,line_width=1, line_dash="dash",
              annotation_text="25%(Sell)", 
              annotation_position="top left")


fig.add_hline(lower_limit,line_width=2, line_dash="dash",line_color="green",
              annotation_text="100%(Buy)", 
              annotation_position="top left")

fig.add_hline(lower_limit1,line_width=2, line_dash="dash",
              annotation_text="75%(Buy)",line_color="orange", 
              annotation_position="top left")

fig.add_hline(lower_limit2,line_width=2, line_dash="dash",
              annotation_text="50%(Buy)", line_color="pink", 
              annotation_position="top left")

fig.add_hline(lower_limit3,line_width=1, line_dash="dash",
              annotation_text="25%(Buy)", 
              annotation_position="top left")

fig.update_layout(plot_bgcolor='white',)
fig.show()


# In[407]:


mergeset["Denormalized_Price"].mean()+4*mergeset["Denormalized_Price"].std()


# In[408]:


import seaborn as sns
sns.distplot(mergeset["Denormalized_Price"])
plt.axvline(upper_limit,linestyle ="--", 
            color ='black')

plt.axvline(lower_limit,linestyle ="--", 
            color ='black')
plt.show()


# In[ ]:


# 
# import pywhatkit
 
 
# pywhatkit.sendwhatmsg("+919764334720", 
#                       "Geeks For Geeks!", 
#                       18, 30)


# In[ ]:


# pip install pywhatkit
# import pywhatkit as kit

# # Specify the phone number (with country code) and the message
# phone_number = "+919764334720"
# message = "Hello from Python! This is an instant WhatsApp message."

# # Send the message instantly
# kit.sendwhatmsg_instantly(phone_number, message)


# In[16]:



import smtplib
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls()
# Authentication
# s.login("tusharkolekar24@gmail.com", "120510986")
# # message to be sent
# message = "Message_you_need_to_send"
# # sending the mail
# s.sendmail("tusharkolekar24@gmail.com", "tusharkolekar24@gmail.com", message)
# # terminating the session
# s.quit()


# In[17]:


s.login("tusharkolekar24@gmail.com", "kyup rsue qpeg winu")


# In[18]:


message = "Message_you_need_to_send.\n Test code Run Succesfully"
# sending the mail
s.sendmail("tusharkolekar24@gmail.com", "tusharkolekar24@gmail.com", message)
# terminating the session
s.quit()


# In[19]:


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
mail_content = '''Hello,
This is a test mail.
In this mail we are sending some attachments.
The mail is sent using Python SMTP library.
Thank You
'''
#The mail addresses and password
sender_address = 'tusharkolekar24@gmail.com'
sender_pass = 'kyup rsue qpeg winu'
receiver_address = 'tusharkolekar24@gmail.com'
#Setup the MIME
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = 'A test mail sent by Python. It has an attachment.'
#The subject line
#The body and the attachments for the mail
message.attach(MIMEText(mail_content, 'plain'))
attach_file_name = r"C:\Users\Tushar\Desktop\code.txt"
attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
payload = MIMEBase('application', 'octate-stream')
payload.set_payload((attach_file).read())
encoders.encode_base64(payload) #encode the attachment
#add payload header with filename
payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
message.attach(payload)
#Create SMTP session for sending the mail
session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
session.starttls() #enable security
session.login(sender_address, sender_pass) #login with mail_id and password
text = message.as_string()
session.sendmail(sender_address, receiver_address, text)
session.quit()
print('Mail Sent')


# In[ ]:




