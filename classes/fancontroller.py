from fan import Fan

class FanController :
    def __init__ (self, ds) :
        print("[FANC] Initialized\n")
        self.ds = ds
        self.fan = Fan()

    def process (self) :
        t = self.ds.get_temperature()
        v = 1 # PID(t)
        self.fan.set(v)
