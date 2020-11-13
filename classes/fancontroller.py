from fan import Fan
from simple_pid import PID

class FanController :
    def __init__ (self, ds, sett) :
        print("[FANC] Initialized")

        # we are cooling, so more fan if we are over temp
        self.pid = PID(Kp=-1.0, output_limits=(0,100))
        self.ds = ds
        self.sett = sett
        self.lastValue = None
        self.fan = Fan()

    def process (self) :
        t = self.ds.get_temperature()

        self.pid.setpoint = self.sett.temperatureSetpoint
        v = self.pid(t)

        if (self.lastValue is None or self.lastValue != v) :
            print("[FANC] Process {} -> {}".format(t, v))

            self.lastValue = v
            self.fan.set(v)
