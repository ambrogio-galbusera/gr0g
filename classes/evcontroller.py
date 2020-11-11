import time

class EVController :
    def __init__ (self, ds) :
        print("[EVC ] Initialized\n")
        self.start_time = time.time()
        self.ev_on = False
        self.on_time = 0
        self.ds = ds

    def process (self) :
        if (self.ev_on) :
            delta = time.time() - self.on_time
            if (delta > 10) :
                print("[EVC ] Closing EV");
                self.ev_on = False
                self.start_time = time.time()
        else :
            delta = time.time() - self.start_time
            if (delta > 10) :
                print("[EVC ] Firing EV");
                self.ev_on = True
                self.on_time = time.time()
