import os
import os.path as path
from typing import Final
from datetime import datetime
from account import account, str_to_account
from ggapis import SCREENSHOTS_FOLDER_ID

APP_LOCATION: Final = 'parentalControl_LocalStorage'
TEMP_IMG: Final = 'images'
APP_TRACK_LOGIN: Final = 'secret'

def mkfolder(parentPath,foldername):
    folderpath = path.join(parentPath,foldername)
    if not path.exists(folderpath):
        os.mkdir(folderpath)

def get_location():
    return path.join(path.expanduser('~'), APP_LOCATION)

def mkapp_local_storage():
    if not path.exists(path.join(path.expanduser('~'), APP_LOCATION)):
        #create folder for app local data
        rawPath = path.expanduser('~')
        mkfolder(rawPath, APP_LOCATION)

        #create folder for temp screen-captures to upload into drive
        appPath = path.join(rawPath, APP_LOCATION)
        mkfolder(appPath, TEMP_IMG)
    return path.join(get_location(), TEMP_IMG)

def note_interrupted(timeInterrupted: datetime, user: account, beingLocked = False):
    f = open(path.join(get_location(), APP_TRACK_LOGIN),'w')
    f.write(f'{timeInterrupted.strftime("%d%m%Y_%H%M%S")}\n')
    f.write(f'{account}\n')
    f.write('LOCKED' if beingLocked else '')

def check_interrupted():
    f = open(path.join(get_location(), APP_TRACK_LOGIN),'r')
    data = f.read().splitlines()
    return (datetime.strptime(data[0].strip(),"%d%m%Y_%H%M%S"),
            str_to_account(data[1].strip()),
            len(data) == 3)