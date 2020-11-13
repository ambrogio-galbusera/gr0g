from scr_home import ScreenHome
from scr_tempgraph import ScreenTemperatureGraph
from scr_humigraph import ScreenHumidityGraph
from scr_lightgraph import ScreenLightGraph
from scr_settings import ScreenSettings

class ScreenManager :
    def __init__ (self, d, ds, sett, kp) :
        print("[SCRM] Initialized")
        self.display = d
        self.ds = ds
        self.sett = sett
        self.keypad = kp
        self.screens = [ScreenHome(d,ds,sett,kp), ScreenTemperatureGraph(d,ds,sett,kp), ScreenHumidityGraph(d,ds,sett,kp), ScreenLightGraph(d,ds,sett,kp), ScreenSettings(d,ds,sett,kp)]
        self.currIdx = 0
        self.currScreen = self.screens[self.currIdx]

    def update (self) :
        self.currScreen.update()

    def process (self) :
        res = self.currScreen.process()

        if (res == 1) :
            if (self.keypad.left_pressed()) : 
                # next screen
                self.currScreen = self.nextScreen()
            elif (self.keypad.right_pressed()) :
                # prev screen
                self.currScreen = self.prevScreen()

            self.currScreen.update()

    def nextScreen (self) :
        self.currIdx = (self.currIdx + 1) % len(self.screens)
        self.currScreen = self.screens[self.currIdx]

    def prevScreen (self) :
        if (self.currIdx == 0) :
            self.currIdx = len(self.screens) - 1
        else :
            self.currIdx = self.currIdx - 1
        self.currScreen = self.screens[self.currIdx]
