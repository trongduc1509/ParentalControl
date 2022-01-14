import os
import os.path as path
import time
from datetime import datetime, timedelta
from threading import Event, Thread
from typing import Final
from account import account, myTime, str_to_myTime
from ggapis import TIME_CONFIG_ID, read_data_file
from process import APP_TRACK_LOGIN, check_interrupted, get_location, mkapp_local_storage, note_interrupted
from ui import checkTimeLeft, error_dialog, info_dialog, login_window, shutdown

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
            return account(myTime(datetime.now(),datetime.now() + timedelta(hours=1),60,NONE,NONE),'PARENT')
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
            
            attempts = 3
            while attempts != 0:
                if login_window() == False:
                    info_dialog('Userright: Child - logged in successfully!')
                    return user
                attempts = attempts - 1
            
            error_dialog('Device will be locked for 10 minutes')
            note_interrupted(datetime.now(), user, True)
            shutdown()


def main():
    user = login()
    is_terminate = Event()
    print(mkapp_local_storage())

    sync_data_thr = Thread(target=update_time_use, args=(is_terminate, user))

    if user.userRight == 'CHILD':
        sync_data_thr.start()
    checkTimeLeft(is_terminate,user)    
    

if __name__ == '__main__':
    main()