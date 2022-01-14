import os
import os.path as path
from typing import Final

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
    #create folder for app local data
    rawPath = path.expanduser('~')
    mkfolder(rawPath, APP_LOCATION)

    #create folder for temp screen-captures to upload into drive
    appPath = path.join(rawPath, APP_LOCATION)
    mkfolder(appPath, TEMP_IMG)
    return path.join(appPath, TEMP_IMG)

