import time
from led import Led
from simple_pid import PID
import pwm2 as rpwm

class LightController :
    def __init__ (self, ds, sett) :
        print("[LIGC] Initialized")
        self.ds = ds
        self.sett = sett
        self.led1 = Led(2)
        self.led2 = Led(3)
        self.isNight = False
        self.startTime = time.time()
        self.lastValue = None
        self.override = False

        rpwm.rpwm_init()

    def set(self, state) :
        print("[LIGC] Setting state to " + repr(state))
        if (state == 0) :
            self.override = True
            v = 0
            self.led1.set(v)
            self.led2.set(v)
            rpwm.rpwm_set(v)
            self.lastValue = v
        elif (state == 1) :
            self.override = True
            v = 100
            self.led1.set(v)
            self.led2.set(v)
            rpwm.rpwm_set(v)
            self.lastValue = v
        elif (state == 2) :
            self.override = False
            self.lastValue = None

    def process (self) :
        # stay on for dayDuration minutes, then off for nightDuration minutes
        #  0-10% of day duration -> dim up
        # 10-90% of day duration -> full
        # 90-100% of day duration -> dim down
        # nightDuration -> off
        if (self.override) :
            return

        delta = time.time() - self.startTime
        v = 0

        if (self.isNight) :
            nightDuration = self.sett.nightDuration * 60
            if (delta > nightDuration) :
                self.isNight = False
                self.startTime = time.time()
            else :
                v = 0
        else :
           dayDuration = self.sett.dayDuration * 60
           dimInterval = dayDuration / 10

           if (delta < dimInterval) :
               v = int((delta / dimInterval) * 100)
           elif (delta > dayDuration) :
               self.isNight = True
               self.startTime = time.time()
           elif (delta > dayDuration - dimInterval) :
               v = int(((dayDuration-delta) / dimInterval) * 100)
           else :
               v = 100

        if (self.lastValue is None or self.lastValue != v) :
            print("[LIGC] Setting LEDs to {}".format(v))
            self.led1.set(v)
            self.led2.set(v)
            rpwm.rpwm_set(v)
            self.lastValue = v
