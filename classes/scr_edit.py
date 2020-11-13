import os
import time


class ScreenEdit :
    # Margins
    margin = 3

    def __init__ (self,d,ds,sett,kp) :
        print("[EDIT] Initialized")
        self.display = d
        self.ds = ds
        self.sett = sett
        self.keypad = kp

    def setProperties(self, title, value, min, max, format, fmt_string) :
        self.title = title
        self.value = value
        self.saveValue = value
        self.min = min
        self.max = max
        self.format = format
        self.fmtString = fmt_string

    def value(self) :
        return self.value

    def process (self) :
        #print("[EDIT] Process")
        if (self.keypad.upPressed()) :
            # increment & update
            self.value += self.step()
            if (self.value > self.max) :
                self.value = self.max

            self.update()
        elif (self.keypad.downPressed()) :
            # decrement & update
            self.value -= self.step()
            if (self.value < self.min) :
                self.value = self.min

            self.update()

        return (self.keypad.rightPressed() or self.keypad.leftPressed())

    def update (self) :
        self.display.drawInit((0,0,0))

        # draw title
        self.display.overlay_text((self.margin, 3), self.title, font_size=1, align_right=False, rectangle=False)

        # draw value
        if (self.format == 0) :
            # number
            value_string = self.fmtString.format(self.value)
        elif (self.format == 1) :
            # time (hours:minutes)
            value_string = self.fmtString.format(int(self.sett.nightDuration/60), int(self.sett.nightDuration%60))
        else :
            value_string = "{}".format(self.value)

        self.display.overlay_text((80, 40), value_string, font_size=2, align_right=True, rectangle=False)

        self.display.update()

    def step (self) :
        if (self.format == 1) :
            return 10;

        return 1
