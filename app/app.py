import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir + "/classes")

import time
import threading
import dbus
import dbus.service
import dbus.mainloop.glib

PYTHON3 = sys.version_info >= (3, 0)
if PYTHON3:
    from gi.repository import GObject as gobject
    from gi.repository import GLib as glib
else:
    import gobject

from lightcontroller import LightController
from condcontroller import CondController
from fancontroller import FanController
from evcontroller import EVController
from datastore import DataStore
from sensors import Sensors
from screenmanager import ScreenManager
from display import Display
from appsettings import AppSettings
from keypad import Keypad
from dbusservice import TheGr0g

class App :
    def __init__ (self) :
        print("[APP ] Initialized\n")
        self.d = Display()
        self.ds = DataStore()
        self.sett = AppSettings()
        self.keypad = Keypad()
        self.sensors = Sensors()
        self.lightc = None #LightController(self.ds, self.sett)
        self.condc = None #CondController(self.ds, self.sett)
        self.fanc = None #FanController(self.ds, self.sett)
        self.evc = None #EVController(self.ds, self.sett)
        self.screenMngr = ScreenManager(self.d, self.ds, self.sett, self.keypad)
        self.screenMngr.update()

        self.processStart = 0
        self.screensStart = 0

    def process (self) :
        delta = time.time() - self.processStart
        if (delta > 1.0) :
            self.ds.add_humidity(self.sensors.humidity())
            self.ds.add_temperature(self.sensors.temperature())
            self.ds.add_lux(self.sensors.lux())

            if (self.lightc != None) :
                self.lightc.process()
            if (self.condc != None) :
                self.condc.process()
            if (self.fanc != None) :
                self.fanc.process()
            if (self.evc != None) :
                self.evc.process()

            self.processStart = time.time()

    def handleScreens (self) :
        delta = time.time() - self.screensStart
        if (delta > 1.0) :
            self.screenMngr.update()
            self.screensStart = time.time()

        self.screenMngr.process()


app = App()

def mainThread(runEvent):
    print ("[MAIN]: started")
    while runEvent.is_set():
        app.process()
        app.handleScreens()
        time.sleep(0.1)

    print ("[MAIN]: exit")
    return

try:
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("com.ag.gr0g", session_bus)
    object = TheGr0g(app.ds, app.sett, app.lightc, session_bus, '/gr0g')

    runEvent = threading.Event()
    runEvent.set()

    mainT = threading.Thread(target=mainThread, args=(runEvent,))
    mainT.start()

    mainloop = gobject.MainLoop()
    print ("Running example service.")
    mainloop.run()

except (KeyboardInterrupt, SystemExit):
    mainloop.quit()
    runEvent.clear()
    mainT.join()
    print("Host: KeyboardInterrupt")

