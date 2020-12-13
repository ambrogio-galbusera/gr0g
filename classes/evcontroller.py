import time
import gertutil as gu

class EVController :
    def __init__ (self, ds, sett) :
        print("[EVC ] Initialized")
        self.start_time = time.time()
        self.ev_on = False
        self.on_time = 0
        self.ds = ds
        self.sett = sett

    def process (self) :
        if (self.ev_on) :
            delta = time.time() - self.on_time
            if (delta > self.sett.sprayTime) :
                print("[EVC ] Closing EV");
                gu.opendrain_set(0, 0);
                self.ev_on = False
                self.start_time = time.time()
        else :
            delta = time.time() - self.start_time
            if (delta > self.sett.sprayPeriod) :
                print("[EVC ] Firing EV");
                gu.opendrain_set(0, 1);
                self.ev_on = True
                self.on_time = time.time()
