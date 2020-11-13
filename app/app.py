import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir + "/classes")

import time
from lightcontroller import LightController
from condcontroller import CondController
from fancontroller import FanController
from evcontroller import EVController
from datastore import DataStore
#from sensors import Sensors
from screenmanager import ScreenManager
from display import Display
from appsettings import AppSettings
from keypad import Keypad

class App :
    def __init__ (self) :
        print("[APP ] Initialized\n")
        self.d = Display()
        self.ds = DataStore()
        self.sett = AppSettings()
        self.keypad = Keypad()
        #self.sensors = Sensors()
        self.lightc = LightController(self.ds, self.sett)
        self.condc = CondController(self.ds, self.sett)
        self.fanc = FanController(self.ds, self.sett)
        self.evc = EVController(self.ds, self.sett)
        self.screenMngr = ScreenManager(self.d, self.ds, self.sett, self.keypad)

        self.processStart = 0
        self.screensStart = 0

    def process (self) :
        delta = time.time() - self.processStart
        if (delta > 1.0) :
            #self.ds.add_humidity(sensors.humidity())
            #self.ds.add_temperature(sensors.temperature())
            #self.ds.add_lux(sensors.lux())

            self.lightc.process()
            self.condc.process()
            self.fanc.process()
            self.evc.process()

            self.processStart = time.time()

    def handleScreens (self) :
        delta = time.time() - self.screensStart
        if (delta > 1.0) :
            self.screenMngr.update()
            self.screensStart = time.time()

        self.screenMngr.process()


app = App()
cntr = 0
while True :
    app.process()
    app.handleScreens()
    time.sleep(0.1)
