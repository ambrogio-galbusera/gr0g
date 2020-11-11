from led import Led

class LightController :
    def __init__ (self, ds) :
        print("[LIGC] Initialized\n")
        self.ds = ds
        self.led1 = Led(2)
        self.led2 = Led(3)

    def process (self) :
        t = self.ds.get_lux()
        v = 1 # PID(t)
        self.led1.set(v)
        self.led2.set(v)
