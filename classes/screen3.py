import os
import time
import pytz
import colorsys
from pytz import timezone
from astral.geocoder import database, lookup
from astral.sun import sun
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class Screen3 :
    # Margins
    margin = 3

    def __init__ (self,d,ds) :
        print("[SCR2] Initialized\n")
        self.display = d
        self.ds = ds

    def update (self) :
        self.display.drawInit((128,128,128))

        path = os.path.dirname(os.path.realpath(__file__))

        # Humidity
        min_humi = 0
        max_humi = 100
        for i in range(self.ds.num_samples) :
            humidity = self.ds.get_humidity(i)

            y = self.calculate_y(humidity, min_humi, max_humi)
            self.display.rect(i, y, 1, 1);

        humidity = self.ds.get_humidity()
        humidity_string = f"{humidity:.0f}%"
        self.display.overlay_text((68, 0), humidity_string, font_large=True, align_right=True, rectangle=True)
        humidity_icon = Image.open(f"{path}/icons/humidity.png")
        self.display.icon((self.margin, 0), humidity_icon)

        self.display.update()

    def calculate_y(self, t, min, max):
        """Calculates the y-coordinate on a parabolic curve, given x."""
        delta = (max - min) + 2 
        y = 1 + ((self.display.HEIGHT-20) / (max - min +2)) * (t-min)

        return int(self.display.HEIGHT-y)



