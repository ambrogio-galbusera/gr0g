from led import Led
from simple_pid import PID

class LightController :
    def __init__ (self, ds, sett) :
        print("[LIGC] Initialized")
        self.ds = ds
        self.sett = sett
        self.pid = PID(0,1,1)
        self.lastValue = None
        self.led1 = Led(2)
        self.led2 = Led(3)

    def process (self) :
        t = self.ds.get_lux()
        v = self.pid(t)

        if (self.lastValue is None or self.lastValue != v) :
            print("[LIGC] Process {} -> {}".format(t, v))

            self.led1.set(v)
            self.led2.set(v)
            self.lastValue = v
