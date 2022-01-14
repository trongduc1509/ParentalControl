from math import ceil
import os
import os.path as path
import time
from datetime import datetime, timedelta
from threading import Event, Thread
from typing import Final
from account import account, myTime, str_to_myTime
from ggapis import TIME_CONFIG_ID, read_data_file
from process import APP_TRACK_LOGIN, check_interrupted, get_location, mkapp_local_storage, note_interrupted
from ui import error_dialog, info_dialog, login_window, on_exit_checkTime, shutdown, tk, on_exit

NONE: Final = -1

def current_usingTime():
    time_configs = read_data_file(TIME_CONFIG_ID).splitlines()
    for single in time_configs:
        now = datetime.now()
        tf = str_to_myTime(single)
        if (tf.check(now)):
            return tf
    return None

def update_time_use(is_terminate: Event, user: account):
    while not is_terminate.is_set():
        user.currentTF = current_usingTime()
        time.sleep(15)

def count_15s(isSave):
    k = 15
    while k != 0:
        time.sleep(1)
        k = k-1
        if isSave():
            break
    if k==0:
        shutdown()

def login():
    if login_window():
        info_dialog('Userright: Parent - logged in successfully!')
        return account(myTime(datetime(2001,1,1,0,0,0),datetime(2001,1,1,23,59,59),60,NONE,NONE),'PARENT')
    else:
        canUse = current_usingTime()
        if canUse == None:
            isSave=False
            thr15s = Thread(target=count_15s,args=(lambda: isSave,))
            thr15s.daemon=True
            thr15s.start()
            while isSave == False:
                if login_window():
                    isSave=True
                    info_dialog('Userright: Parent - logged in successfully!')
            return account(myTime(datetime.now().replace(2001,1,1),datetime.now().replace(2001,1,1) + timedelta(hours=1),60,NONE,NONE),'PARENT')
        else:
            #check interrupted since last logged in as child account
            user = account(canUse, 'CHILD')
            if (path.exists(path.join(get_location(), APP_TRACK_LOGIN))):
                (lastTime, lastUA, lastCheckLock) = check_interrupted()
                if lastCheckLock and (datetime.now() - lastTime).total_seconds <= 60*10:
                    error_dialog(f'Locked since {lastTime.strftime("%d%m%Y_%H%M%S")} for 10 minutes')
                    shutdown()

                if canUse == lastUA.currentTF:
                    user = lastUA
            return user
            

def checkTimeLeft(is_terminate: Event,user: account):
    root = tk.Tk()
    root.title('C-Program')
    timeLabel = tk.Label(root, font=('Arial Bold',16))
    timeLabel.pack()
    lastTime = datetime.now().replace(2001,1,1)
    def setLabel(lastTime: datetime,is_terminate: Event,user: account):
        while ((user.currentTF.end.replace(2001,1,1) - datetime.now().replace(2001,1,1)).total_seconds() >= 0) and not is_terminate.is_set():
            currentTime = datetime.now().replace(2001,1,1)
            timeLabel.config(text=f'Time left: {(datetime.utcfromtimestamp((user.currentTF.end - currentTime).total_seconds())).strftime("%H:%M:%S")}')
            dt = (currentTime - lastTime).total_seconds()
            lastTime = currentTime
            user.currentUsed += dt
            user.usedInTF += dt

            assert user.currentTF != None
            
            if (user.currentTF.duration == NONE):
                if (user.currentTF.sum != NONE):
                    if (user.currentTF.sum*60 - user.usedInTF) <= 60:
                        if user.userRight == 'PARENT':
                            user = login()
                    
                    if (user.currentTF.sum*60 < user.usedInTF):
                        if user.userRight == 'CHILD':
                            note_interrupted(currentTime, user)
                        is_terminate.set()
                else:
                    if (user.currentTF.end - currentTime).total_seconds() <= 60:
                        if user.userRight == 'PARENT':
                            user = login()
                    
                    if (user.currentTF.end - currentTime).total_seconds() == 0:
                        if user.userRight == 'CHILD':
                            note_interrupted(currentTime, user)
                        is_terminate.set()
            else:
                if (user.currentTF.duration*60 - user.currentUsed) <= 60:
                    if user.userRight == 'PARENT':
                        user = login()
                if (user.currentTF.duration*60 < user.currentUsed):
                    if user.userRight == 'CHILD':
                        note_interrupted(currentTime, user)
                    is_terminate.set()

            time.sleep(1)
        is_terminate.set()
        root.destroy()
    setTextThr = Thread(target=setLabel,args=(lastTime,is_terminate,user))
    setTextThr.daemon = True
    setTextThr.start()
    root.protocol('WM_DELETE_WINDOW', lambda: on_exit_checkTime(root, is_terminate))
    root.mainloop()
    note_interrupted(datetime.now().replace(2001,1,1), user)

def main():
    user = login()
    is_terminate = Event()
    mkapp_local_storage()

    sync_data_thr = Thread(target=update_time_use, args=(is_terminate, user))

    if user.userRight == 'CHILD':
        sync_data_thr.start()
    checkTimeLeft(is_terminate,user)

    if(is_terminate.is_set()):
        shutdown()  
    

if __name__ == '__main__':
    main()