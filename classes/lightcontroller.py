from led import Led
from simple_pid import PID

class LightController :
    def __init__ (self, ds) :
        print("[LIGC] Initialized\n")
        self.ds = ds
        self.pid = PID(0,1,1)
        self.led1 = Led(2)
        self.led2 = Led(3)

    def process (self) :
        t = self.ds.get_lux()
        v = self.pid(t)

        print("[LIGC] Process {} -> {}".format(t, v))
        self.led1.set(v)
        self.led2.set(v)
