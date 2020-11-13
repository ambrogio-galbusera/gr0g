import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir + "/external")

from condenser import Condenser
from simple_pid import PID

class CondController :
    def __init__ (self, ds, sett) :
        print("[CONC] Initialized")
        self.ds = ds
        self.sett = sett
        self.pid = PID(Kp=1, output_limits=(0,100));
        self.lastValue = None
        self.condenser = Condenser()

    def process (self) :
        t = self.ds.get_humidity()

        self.pid.setpoint = self.sett.humiditySetpoint
        v = self.pid(t)

        if (self.lastValue is None or self.lastValue != v) :
            print("[CONC] Process {} -> {}".format(t,v))

            self.condenser.set(v)
            self.lastValue = v
