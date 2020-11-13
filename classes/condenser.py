import gertutil as gu

class Condenser:
    cond_channel = 0
    cond_freq = 1000

    def __init__ (self) :
        print("[COND] PWM brushed on board {}, channel {}".format(gu.board, self.cond_channel))
        gu.pwm_init(self.cond_channel)
        gu.pwm_set(self.cond_channel,self.cond_freq,0)

    def set (self,dc) :
        print("[COND] Setting PWM to {}".format(dc))
        gu.pwm_set(self.cond_channel,self.cond_freq,dc)

    def off (self) :
        print("[COND] Power off")
        gu.pwm_off(self.cond_channel)

