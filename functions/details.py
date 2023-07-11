'''
    This file will contain all the read only functions, that provide information about the system
'''

import os

def getFiles():
    return list(os.listdir("."))

def getDetails():

    # details = []

    for file in os.listdir():
        statinfo = os.stat(file)
        print(file, statinfo.st_size)