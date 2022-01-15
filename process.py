import os
import os.path as path
from time import sleep
from typing import Final
from datetime import datetime
from account import account, str_to_account
from ggapis import upload_cloud_imagefile
from threading import Event
import pyautogui

APP_LOCATION: Final = 'parentalControl_LocalStorage'
TEMP_IMG: Final = 'images'
APP_TRACK_LOGIN: Final = 'secret.txt'

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
    f.write(f'{user}\n')
    f.write('LOCKED' if beingLocked else '')

def check_interrupted():
    f = open(path.join(get_location(), APP_TRACK_LOGIN),'r')
    data = f.read().splitlines()
    return (datetime.strptime(data[0].strip(),"%d%m%Y_%H%M%S"),
            str_to_account(data[1].strip()),
            len(data) == 3)

def screenshot_and_upload(is_terminate: Event):
    today_folder_name = datetime.now().strftime('%m%d%Y')
    mkfolder(path.join(get_location(), TEMP_IMG), today_folder_name)
    today_folder_location = path.join(path.join(get_location(), TEMP_IMG), today_folder_name)
    while not is_terminate.is_set():
        sleep(60)
        busted = datetime.now().strftime('%m%d%Y_%H%M%S')
        localPath = path.join(today_folder_location, f'{busted}.png')
        pyautogui.screenshot(localPath)
        upload_cloud_imagefile(today_folder_name,busted,localPath)
