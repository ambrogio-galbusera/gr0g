from condenser import Condenser

class CondController :
    def __init__ (self, ds) :
        print("[CONC] Initialized\n")
        self.ds = ds
        self.condenser = Condenser()

    def process (self) :
        t = self.ds.get_humidity()
        v = 1 # PID(t)
        self.condenser.set(v)
