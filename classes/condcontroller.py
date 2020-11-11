import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir + "/external")

from condenser import Condenser
from simple_pid import PID

class CondController :
    def __init__ (self, ds) :
        print("[CONC] Initialized\n")
        self.ds = ds
        self.pid = PID(0,1,1);
        self.condenser = Condenser()

    def process (self) :
        t = self.ds.get_humidity()
        v = self.pid(t)

        print("[CONC] Process {} -> {}".format(t,v))
        self.condenser.set(v)
