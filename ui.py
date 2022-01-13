from os import system
import time
import sys
import os
from datetime import datetime
from threading import Event, Thread

import tkinter as tk
from tkinter import Button, ttk
from tkinter.constants import CENTER
from tkinter.messagebox import showerror, showinfo
from turtle import title

def shutdown():
    print('System exit')
    sys.exit()
    #os.system('shutdown /s /t 0')

def on_exit(win: tk.Tk):
    print('Unexpected quit')
    win.destroy()
    #os.system('shutdown /s /t 0')

def login_window():
    root = tk.Tk()
    tempPwd = tk.StringVar()
    #setup root 
    root.attributes('-fullscreen', True)
    root.title("Login")

    #some Events to check User-right, closing app, 

    #widgets
    frame = tk.Frame(root)
    tk.Label(frame, text='PARENTAL-CONTROL APPLICATION', font=('Arial Bold',16)).grid(row=0,column=0,columnspan=2,pady=(0, 20))
    tk.Label(frame, text='Enter password to signin:').grid(row=1,column=0,sticky='w')
    password_entry = tk.Entry(frame,textvariable=tempPwd,show='*').grid(row=1, column=1,columnspan=3,ipadx=30,pady=5)
    signinBtn = tk.Button(frame, text='Sign in').grid(row=2,column=0,columnspan=2,pady=5,sticky='e')

    frame.pack()
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    #start
    root.mainloop()

def checkTimeLeft():
    print()

def error_dialog(err: str):
    showerror(title='Error',message=err)

def info_dialog(info: str):
    showinfo(title='Information',message=info)

if __name__ == '__main__':
    print()