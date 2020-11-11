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

class App :
    def __init__ (self, ds) :
        print("[APP ] Initialized\n")
        self.d = Display()
        self.ds = DataStore()
        #self.sensors = Sensors()
        self.lightc = LightController(self.ds)
        self.condc = CondController(self.ds)
        self.fanc = FanController(self.ds)
        self.evc = EVController(self.ds)
        self.screenMnrgr = ScreenManager(self.d, self.ds)

    def process (self) :
        #self.ds.add_humidity(sensors.humidity())
        #self.ds.add_temperature(sensors.temperature())
        #self.ds.add_lux(sensors.lux())

        self.lightc.process()
        self.condc.process()
        self.fanc.process()
        self.evc.process()

    def handleScreens (self) :
        self.screenMnrgr.process()



ds = DataStore()
app = App(ds)
while True :
    app.process()
    app.handleScreens()
    time.sleep(1)
