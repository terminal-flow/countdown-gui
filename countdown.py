import time
import datetime
import os
import smtplib
from email.message import EmailMessage
from tkinter import *
import tkinter

#change directory into countown-gui/
os.chdir(f'{os.path.dirname(os.path.abspath(__file__))}/')

#variables
dark = False
mail = 'closed'
date = None
settings = False
theme = 'Light'
days_till = False
hours_till = False
minutes_till = False
seconds_till = False
mail_get = False
mail_info = None
counter = 0
email_sent = False

#startup defines
def date_entry():
    global date
    e_day = d_box.get()
    e_month = m_box.get()
    e_year = y_box.get()

    date = str(e_day) + ',' + str(e_month) + ',' + str(e_year)
    if e_day == '' or e_month == '' or e_year == '':
        pass
    else:
        first.destroy()

#start first gui
first = Tk()
first.title('Enter Date')

#default text
d_box = Entry(first, foreground= 'black', background= 'white', width= 5, justify= CENTER)
d_box.insert(0, 'Day')
m_box = Entry(first, foreground= 'black', background = 'white', width= 5, justify= CENTER)
m_box.insert(0, 'Month')
y_box = Entry(first, foreground= 'black', background= 'white', width= 10, justify= CENTER)
y_box.insert(0, 'Year')
entry_btn = Button(first, text= 'Enter', command= date_entry, width= 10, height= 1)

def some_callback(event):
    d_box.delete(0, END)
    m_box.delete(0, END)
    y_box.delete(0, END)
    return None

d_box.bind('<Button-1>', some_callback)
m_box.bind('<Button-2>', some_callback)
y_box.bind('<Button-3>', some_callback)

d_box.grid(row= 0, column= 0)
m_box.grid(row=0, column= 1)
y_box.grid(row=0, column= 2)
entry_btn.grid(row= 0, column= 3)

#if no correct input, carry on
if date == None:
    first.mainloop()

time.sleep(0.5)

#setting core variables
try:
    date = date.split(',')
    day, month, year = date
    day, month, year = int(day), int(month), int(year)
except:
    exit()

year_now = datetime.datetime.now().year
month_now = datetime.datetime.now().month
day_now = datetime.datetime.now().day
hour_now = datetime.datetime.now().hour
minute_now = datetime.datetime.now().minute
second_now = datetime.datetime.now().second

#catch any error
isValidDate = True
try:
    datetime.datetime(year, month, day)
except ValueError:
    isValidDate = False
if isValidDate is False or (year, month, day) < (year_now, month_now, day_now):
    isValidDate = False
    top = Tk()
    top.title('Error')
    top.geometry('400x300')
    error_label = Label(top, text= 'Invalid Date', foreground= 'red', font= ('Arial', 20), height= 7)
    error_label.pack()
    def error_click():
        top.destroy()
        exit()
    error_btn = Button(top, text= 'Quit', foreground= 'red', command= error_click, font= ('Arial', 20))
    error_btn.pack()
    top.mainloop()

#start main gui
if isValidDate == False:
    exit()
root = Tk()
root.title('Time \'Till')
root.configure(background= 'white')

#email setup
#possible to use os.environ in .zshrc
file = open('email/email_a.txt', 'r')
email_address = file.read().strip()
file.close()

file = open('email/email_p.txt', 'r')
email_password = file.read().strip()
file.close()

msg = EmailMessage()
msg['Subject'] = 'Countdown Alert'
msg['From'] = 'Countdown'

def main_loop():

    hour_now = datetime.datetime.now().hour
    minute_now = datetime.datetime.now().minute
    second_now = datetime.datetime.now().second

    global days_till
    global hours_till
    global minutes_till
    global seconds_till

    days_till = (datetime.datetime(year, month, day) - datetime.datetime.now()).days
    days = '  Days  '

    hours_till = 23 - hour_now
    hours = '  Hours  '

    minutes_till = 59 - minute_now
    minutes = '  Minutes  '

    seconds_till = 59 - second_now
    seconds = '  Seconds  '

    if days_till == 1:
        days = '  Day  '
    if hours_till == 1:
        hours = '  Hour  '
    if minutes_till == 1:
        minutes = '  Minute  '
    if seconds_till == 1:
        seconds = '  Second  '

    #converting into strings
    days_till = str(days_till)
    hours_till = str(hours_till)
    hour_now = str(hour_now)
    minutes_till = str(minutes_till)
    minute_now = str(minute_now)
    seconds_till = str(seconds_till)
    second_now = str(second_now)

    if days_till <= '-1':
        time_till = ('0  Days  0  Hours  0  Minutes  0  Seconds  ')
    else:
        time_till = (days_till + days + hours_till + hours + minutes_till + minutes 
        + seconds_till + seconds)

    #main countdown
    #------dark---------
    if dark == True:
        timeT_label = Label(root, text= time_till, width= 40, height= 5, foreground = 'white', background = 'black')
        timeT_label.config(font= ('Arial', 40))

    #------light---------
    else:
        timeT_label = Label(root, text= time_till, width= 40, height= 5, foreground = 'black', background = 'white')
        timeT_label.config(font= ('Arial', 40))

    #placing
    if days_till <= '-1':
        timeT_label.config(foreground= 'red')

    timeT_label.grid(row= 1, column= 0, padx= 50, pady= 5, rowspan= 4, columnspan = 3)

    #no overlapping
    root.after(1000, main_loop)
    root.after(1000, timeT_label.destroy)

days_till2 = (datetime.datetime(year, month, day) - datetime.datetime.now()).days
days_till2 = str(days_till2)

def mail_loop():
    global days_till
    global days_till2
    global hours_till
    global minutes_till
    global seconds_till
    global email_sent

    #email check
    if seconds_till == '1':
        days_till2 = (datetime.datetime(year, month, day) - datetime.datetime.now()).days
        days_till2 = str(days_till2)
        email_sent = False

    def sending_mail():
        msg.set_content(days_till)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
        root.after(3000)

    #send mail
    if mail == 'open':
        if days_till == '0' and hours_till == '0' and minutes_till == '0' and seconds_till == '0' and email_sent != True:
            days_till = 'It is now the date you set!'
            sending_mail()
            email_sent = True
            exit()
        elif days_till != days_till2 and email_sent != True:
            days_till = 'There is only ' + days_till2 + ' days left!'
            email_sent = True
            sending_mail()
    root.after(1000, mail_loop)

#settings
settings_menu = Label(root, background= 'white', height= 15, width= 35)

#Settings core defines
def settings_func():
    global settings
    global mail_info
    if settings == True:
        settings = False
        settings_menu.grid_remove()
        theme_btn.grid_remove()
        theme_label.grid_remove()
        mail_btn.grid_remove()
        mail_label.grid_remove()
        mail_ent.grid_remove()
        mail_ent_btn.grid_remove()
        mail_info.grid_remove()
    else:
        settings = True

def shade(main_loop):
    global dark
    global settings_menu
    if dark == True:
        root.config(background= 'white')
        settings_menu.config(background= 'white')
        dark = False
        #delay for sync
        #root.after(1000)
        
    else:
        root.config(background= 'black')
        settings_menu.config(background= 'black')
        dark = True
        #delay for sync
        #root.after(1000)

def theme_stat():
    global theme
    if theme == 'Light':
        theme = 'Dark'
        theme_label.config(foreground= 'white', background= 'black')
        theme_btn.config(text= 'Dark')
        mail_label.config(foreground= 'white', background= 'black')
        mail_ent.config(foreground= 'white', background= 'black')
        if mail_info != None:
            mail_info.config(foreground= 'white', background= 'black')
    else:
        theme = 'Light'
        theme_label.config(foreground= 'black', background= 'white')
        theme_btn.config(text= 'Light')
        mail_label.config(foreground= 'black', background= 'white')
        mail_ent.config(foreground= 'black', background= 'white')
        if mail_info != None:
            mail_info.config(foreground= 'grey', background= 'white')

def mail_func():
    global mail
    if mail == 'closed':
        mail = 'open'
        mail_btn.config(text= 'On')
    else:
        mail = 'closed'
        mail_btn.config(text= 'Off')

def mail_ent_func():
    global mail
    global mail_info
    global counter
    global theme
    mail_get = mail_ent.get()
    for letter in mail_get:
        if letter == '@':
            counter = 1
            del letter
        else:
            pass
    if mail_info != None and len(mail_get) > 5 and counter == 1 and email_address != '' and email_password != '':
        mail_info.destroy()
    if len(mail_get) > 5 and counter == 1 and email_address != '' and email_password != '':
        mail_btn.config(state= NORMAL)
        mail = 'closed'
        mail_func()
        del msg['To']
        msg['To'] = mail_get
        if theme == 'Dark':
            mail_info = Label(root, text= 'Your current email is: ' + msg['To'], foreground= 'white', background= 'black')
        else:
            mail_info = Label(root, text= 'Your current email is: ' + msg['To'], foreground= 'gray')
        mail_info.grid(row= 4, column= 4, columnspan= 2)
        del mail_get
    counter = 0
    mail_ent.delete(0, END)

theme_btn = Button(root, text= 'Light', font= ('Arial', 20), command= lambda: [shade(main_loop()), theme_stat()])
theme_label = Label(root, text= 'Theme:', font= ('Arial', 20))
if msg['To'] == None:
    mail_btn = Button(root, text= 'Off', font= ('Arial', 20), command= mail_func, state= DISABLED)
else:
    mail_btn = Button(root, text= 'Off', font= ('Arial', 20), command= mail_func)
mail_label = Label(root, text= 'Email:', font= ('Arial', 20))
mail_ent = Entry(root, width= 20)
mail_ent_btn = Button(root, text= 'Enter', justify= CENTER, command= mail_ent_func)
if theme == 'Dark':
    mail_info = Label(root, text= 'Your current email is: None', foreground= 'white', background= 'black')
else:
    mail_info = Label(root, text= 'Your current email is: None', foreground= 'gray')
settings_btn = Button(root, text= 'Settings', foreground= 'black', background= 'white', command= lambda: [(theme_btn.grid(row= 1, column= 5),
                                                                                                            settings_menu.grid(row= 0, column= 3, rowspan= 4, columnspan= 8),
                                                                                                            theme_label.grid(row= 1, column= 4)),
                                                                                                            mail_btn.grid(row= 2, column= 5),
                                                                                                            mail_label.grid(row= 2, column= 4),
                                                                                                            mail_ent.grid(row= 3, column= 4),
                                                                                                            mail_ent_btn.grid(row= 3, column= 5),
                                                                                                            mail_info.grid(row= 4, column= 4, columnspan= 2),
                                                                                                            settings_func()])

settings_btn.grid(row= 0, column= 2, pady= 10)

mail_loop()
main_loop()
root.mainloop()
