from os import system
import time
import sys
import os
from datetime import datetime
from threading import Event, Thread

import tkinter as tk
from tkinter.constants import CENTER
from tkinter.messagebox import showerror, showinfo
from turtle import title

from account import account

from ggapis import ACCOUNT_DATA_ID, read_data_file
from process import note_interrupted

def shutdown():
    #sys.exit()
    os.system('shutdown /s /t 1')

def on_exit(win: tk.Tk):
    #print('Unexpected quit')
    #win.destroy()
    os.system('shutdown /s /t 1')

def on_exit_checkTime(win: tk.Tk, is_terminate: Event):
    is_terminate.set()

def login_window():
    root = tk.Tk()
    tempPwd = tk.StringVar()
    #setup root 
    root.attributes('-fullscreen', True)
    root.title("Login")

    #some Events to check User-right, closing app
    isRunning = Event()
    isSupervisor = Event()

    #widgets
    frame = tk.Frame(root)
    tk.Label(frame, text='PARENTAL-CONTROL APPLICATION', font=('Arial Bold',16)).grid(row=0,column=0,columnspan=2,pady=(0, 20))
    tk.Label(frame, text='Enter password to signin:').grid(row=1,column=0,sticky='w')
    password_entry = tk.Entry(frame,textvariable=tempPwd,show='*').grid(row=1, column=1,columnspan=3,ipadx=30,pady=5)
    shutdownBtn = tk.Button(frame, text='Shut down', command=shutdown).grid(row=2,column=0,columnspan=2,pady=5,sticky='w')
    signinBtn = tk.Button(frame, text='Sign in',command= lambda: check_pass(tempPwd,root,isRunning,isSupervisor)).grid(row=2,column=0,columnspan=2,pady=5,sticky='e')

    frame.pack()
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    #close app -> shutdown
    root.protocol('WM_DELETE_WINDOW', lambda: on_exit(root))

    #start
    root.mainloop()

    return isSupervisor.is_set()

def check_pass(password: tk.StringVar, root: tk.Tk, isRunning: Event, isSupervisor: Event):
    pwd = password.get()
    pwd_storage = read_data_file(ACCOUNT_DATA_ID).splitlines()
    for single in pwd_storage:
        m = single.split()
        if m[0] == pwd:
            isRunning.set()
            if m[1] == 'PARENT':
                isSupervisor.set()
    if isRunning.is_set():
        root.destroy()

def error_dialog(err: str):
    showerror(title='Error',message=err)

def info_dialog(info: str):
    showinfo(title='Information',message=info)

if __name__ == '__main__':
    #checkTimeLeft(datetime(2001,1,1,16,50,0))
    print()