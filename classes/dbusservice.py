import sys

PYTHON3 = sys.version_info >= (3, 0)
if PYTHON3:
    from gi.repository import GObject as gobject
    from gi.repository import GLib as glib
else:
    import gobject

import dbus
import dbus.service
import dbus.mainloop.glib

class TheGr0g(dbus.service.Object):

    def __init__(self, ds, sett, lightc, bus, path) :
        self.ds = ds
        self.sett = sett
        self.lightc = lightc
        super(TheGr0g, self).__init__(bus, path)

    @dbus.service.method("com.ag.gr0g",
                         in_signature='', out_signature='a{sd}')
    def status(self):
        print ("[DBUS] status")
        return { "temperature": self.ds.get_temperature(),
                 "humidity": self.ds.get_humidity(),
                 "light": self.ds.get_lux(),
                 "temperature_setpoint": self.sett.temperatureSetpoint,
                 "humidity_setpoint": self.sett.humiditySetpoint }

    @dbus.service.method("com.ag.gr0g",
                         in_signature='s', out_signature='a{ss}')
    def cmd(self, data):
        print ("[DBUS] cmds " + repr(data))
        cmd = data["cmd"]
        value = data["state"]
        print ("cmds " + cmd +":" + value)
        if (cmd == "setlight") :
            if (self.lightc != None) :
                self.lightc.set(int(value))
        elif (cmd == "humidity_setpoint") :
            self.sett.humiditySetpoint = value
        elif (cmd == "temperature_setpoint") :
            self.sett.temperatureSetpoint = value

        return { "result": "OK" }


