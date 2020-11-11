import gertutil as gu

class Fan:
    fan_channel = 0
    fan_freq = 1000

    def __init__ (self) :
        print("[FAN ] PWM brushed on board {}, channel {}\n".format(gu.board, self.fan_channel))
        gu.pwm_init(self.fan_channel)
        gu.pwm_set(self.fan_channel,self.fan_freq,0)

    def set (self,dc) :
        print("[FAN ] Setting PWM to {}\n".format(dc))
        gu.pwm_set(self.fan_channel,self.fan_freq,dc)

    def off (self) :
        print("[FAN ] Power off\n")
        gu.pwm_off(self.fan_channel)

