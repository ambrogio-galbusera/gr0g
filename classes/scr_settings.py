import os
import time
from scr_edit import ScreenEdit

class ScreenSettings :
    # Margins
    margin = 3

    def __init__ (self,d,ds,sett,kp) :
        print("[SETT] Initialized")
        self.display = d
        self.ds = ds
        self.sett = sett
        self.keypad = kp
        self.subIdx = -1
        self.subScreen = None

    def process (self) :
        print("[SETT] Process")
        if (self.subIdx != -1) :
            # editing settings
            self.subScreen.process()

            if (self.keypad.rightPressed()) :
                # next screen
                self.saveValue()

                if (self.subIdx < 6) :
                    self.subIdx = self.subIdx + 1
                    self.subScreen = self.initEditScreen(self.subIdx)
                    self.subScreen.update()
                else :
                    self.subIdx = -1
                    self.update()
            elif (self.keypad.leftPressed()) :
                # prev screen
                self.saveValue()

                if (self.subIdx > 0) :
                    self.subIdx = self.subIdx - 1
                    self.subScreen = self.initEditScreen(self.subIdx)
                    self.subScreen.update()
                else :
                    self.subIdx = -1
                    self.update()

        else :
#            if (self.keypad.downPressed()) :
             if (True) :
                self.subIdx = 0
                self.subScreen = self.initEditScreen(self.subIdx)
                self.subScreen.update()

        return (self.keypad.rightPressed() or self.keypad.leftPressed())

    def update (self) :
        if (self.subIdx != -1) :
            self.subScreen.update()
            return

        self.display.drawInit((0,0,0))

        value_string = "{0:01d}:{1:02d}".format(int(self.sett.dayDuration/60), int(self.sett.dayDuration%60))
        self.display.overlay_text((self.margin, 3), "Day duration", font_size=0, align_right=False, rectangle=False)
        self.display.overlay_text((100, 3), value_string, font_size=1, align_right=True, rectangle=False)

        value_string = "{0:01d}:{1:02d}".format(int(self.sett.nightDuration/60), int(self.sett.nightDuration%60))
        self.display.overlay_text((self.margin, 15), "Night duration", font_size=0, align_right=False, rectangle=False)
        self.display.overlay_text((100, 15), value_string, font_size=1, align_right=True, rectangle=False)

        value_string = "{0:3d}".format(int(self.sett.sprayPeriod))
        self.display.overlay_text((self.margin, 27), "Spray period (s)", font_size=0, align_right=False, rectangle=False)
        self.display.overlay_text((100, 27), value_string, font_size=1, align_right=True, rectangle=False)

        value_string = "{0:3d}".format(int(self.sett.sprayTime))
        self.display.overlay_text((self.margin, 39), "Spray time (s)", font_size=0, align_right=False, rectangle=False)
        self.display.overlay_text((100, 39), value_string, font_size=1, align_right=True, rectangle=False)

        value_string = f"{self.sett.temperatureSetpoint:.0f}°C"
        self.display.overlay_text((self.margin, 51), "Temperature", font_size=0, align_right=False, rectangle=False)
        self.display.overlay_text((100, 51), value_string, font_size=1, align_right=True, rectangle=False)

        value_string = f"{self.sett.humiditySetpoint:.0f}%"
        self.display.overlay_text((self.margin, 63), "Humidity", font_size=0, align_right=False, rectangle=False)
        self.display.overlay_text((100, 63), value_string, font_size=1, align_right=True, rectangle=False)

        self.display.update()

    def initEditScreen (self, idx):
        scr = ScreenEdit(self.display, self.ds, self.sett, self.keypad)

        if (idx == 0) :
            scr.setProperties(title="Day duration", value=self.sett.dayDuration, min=0, max=1440, format=1, fmt_string="{0:02d}:{1:02d}")
        elif (idx == 1) :
            scr.setProperties(title="Night duration", value=self.sett.nightDuration, min=0, max=1440, format=1, fmt_string="{0:02d}:{1:02d}")
        elif (idx == 2) :
            scr.setProperties(title="Spray period", value=self.sett.sprayPeriod, min=0, max=999, format=0, fmt_string="{0:03d}")
        elif (idx == 3) :
            scr.setProperties(title="Spray time", value=self.sett.sprayTime, min=0, max=999, format=0, fmt_string="{0:03d}")
        elif (idx == 4) :
            scr.setProperties(title="Temperature", value=self.sett.temperatureSetpoint, min=0, max=1440, format=0, fmt_string="{0:02d}°C")
        elif (idx == 5) :
            scr.setProperties(title="Day duration", value=self.sett.humiditySetpoint, min=0, max=100, format=0, fmt_string="{0:02d}%")

        return scr

    def saveValue (self) :
        if (idx == 0) :
            self.sett.dayDuration = self.subScreen.value()
        elif (idx == 1) :
            self.sett.nightDuration = self.subScreen.value()
        elif (idx == 2) :
            self.sett.sprayPeriod = self.subScreen.value()
        elif (idx == 3) :
            self.sett.sprayTime = self.subScreen.value()
        elif (idx == 4) :
            self.sett.temperatureSetpoint = self.subScreen.value()
        elif (idx == 5) :
            self.sett.humiditySetpoint = self.subScreen.value()

        self.sett.save()

