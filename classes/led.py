import gertutil as gu

class Led:
    led_freq = 1000

    def __init__ (self, ch) :
        self.led_channel = ch
        print("[LED ] PWM brushed on board {}, channel {}".format(gu.board, self.led_channel))
        gu.pwm_init(self.led_channel)
        gu.pwm_set(self.led_channel,self.led_freq,0)

    def set (self,dc) :
        #print("[LED ] Setting PWM to {}".format(dc))
        gu.pwm_set(self.led_channel,self.led_freq,dc)

    def off (self) :
        print("[LED ] Power off")
        gu.pwm_off(self.led_channel)

