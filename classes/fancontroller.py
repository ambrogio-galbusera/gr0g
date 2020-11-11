from fan import Fan
from simple_pid import PID

class FanController :
    def __init__ (self, ds) :
        print("[FANC] Initialized\n")
        self.pid = PID(0,1,1)
        self.ds = ds
        self.fan = Fan()

    def process (self) :
        t = self.ds.get_temperature()
        v = self.pid(t)

        print("[FANC] Process {} -> {}".format(t, v))
        self.fan.set(v)
