from DrissionPage import ChromiumPage, ChromiumOptions
from time import sleep
import random
import os
import shutil
import threading

dir_path = os.path.dirname(os.path.realpath(__file__))
sep = os.sep

def getDriver():
    options = ChromiumOptions()
    local_port = random.randint(1000, 9999)
    print(local_port)
    options.set_paths(local_port=local_port)
    options.set_user_data_path(dir_path +sep + 'profiles')
    page = ChromiumPage(options)
    return page