import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir + "/classes")

import time
from evcontroller import EVController
from appsettings import AppSettings
from datastore import DataStore

ds = DataStore()
sett = AppSettings()
evc = EVController(ds, sett)

while (True) :
    evc.process()
    time.sleep(1)
