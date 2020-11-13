import os
import time
import pytz
import colorsys
from pytz import timezone
from astral.geocoder import database, lookup
from astral.sun import sun
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class ScreenTemperatureGraph :
    # Margins
    margin = 3

    def __init__ (self,d,ds,sett,kp) :
        print("[TMPG] Initialized")
        self.display = d
        self.ds = ds
        self.sett = sett
        self.keypad = kp

    def process (self) :
        print("[TMPG] TODO")

    def update (self) :
        self.display.drawInit((128,128,128))

        path = os.path.dirname(os.path.realpath(__file__))

        # Temperature
        min_temp = None
        max_temp = None
        for i in range(self.ds.num_samples) :
            temperature = self.ds.get_temperature(i)

            if min_temp is not None and max_temp is not None:
                if temperature < min_temp:
                    min_temp = temperature
                elif temperature > max_temp:
                    max_temp = temperature
            else:
                min_temp = temperature
                max_temp = temperature

        for i in range(self.ds.num_samples) :
            temperature = self.ds.get_temperature(i)

            y = self.calculate_y(temperature, min_temp, max_temp)
            self.display.rect(i, y, 1, 1);

        temperature = self.ds.get_temperature()
        temp_string = f"{temperature:.0f}°C"
        self.display.overlay_text((80, 0), temp_string, font_size=2, align_right=True, rectangle=True)
        spacing = self.display.font.getsize(temp_string)[1] + 1
        if min_temp is not None and max_temp is not None:
            range_string = f"{min_temp:.0f}-{max_temp:.0f}"
        else:
            range_string = "------"
        self.display.overlay_text((80, 0 + spacing), range_string, font_size=2, align_right=True, rectangle=True)
        temp_icon = Image.open(f"{path}/icons/temperature.png")
        self.display.icon((self.margin, 0), temp_icon)

        self.display.update()

    def calculate_y(self, t, min, max):
        """Calculates the y-coordinate on a parabolic curve, given x."""
        delta = (max - min) + 2 
        y = 1 + ((self.display.HEIGHT-20) / (max - min +2)) * (t-min)

        return int(self.display.HEIGHT-y)



