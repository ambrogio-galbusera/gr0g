from screen1 import Screen1
from screen2 import Screen2

class ScreenManager :
    def __init__ (self, d, ds) :
        print("[SCRM] Initialized\n")
        self.display = d
        self.ds = ds
        self.screen1 = Screen1(d, ds)
        self.screen2 = Screen2(d, ds)
        self.screens = [self.screen1, self.screen2]
        self.currIdx = 0
        self.currScreen = self.screens[self.currIdx]

    def process (self) :
        res = self.currScreen.process()
        if (res == 1) :
            # next screen
            self.currScreen = self.nextScreen()
        elif (res == -1) :
            # prev screen
            self.currScreen = self.prevScreen()

    def nextScreen (self) :
        self.currIdx = (self.currIdx + 1) % len(self.screens)
        self.currScreen = self.screens[self.currIdx]

    def prevScreen (self) :
        if (self.currIdx == 0) :
            self.currIdx = len(self.screens) - 1
        else :
            self.currIdx = self.currIdx - 1
        self.currScreen = self.screens[self.currIdx]
