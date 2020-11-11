import os
import time
import pytz
import colorsys
from pytz import timezone
from astral.geocoder import database, lookup
from astral.sun import sun
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class Screen4 :
    # Margins
    margin = 3

    def __init__ (self,d,ds) :
        print("[SCR2] Initialized\n")
        self.display = d
        self.ds = ds

    def update (self) :
        self.display.drawInit((128,128,128))

        path = os.path.dirname(os.path.realpath(__file__))

        # Lux
        min_lux = None
        max_lux = None
        for i in range(self.ds.num_samples) :
            lux = self.ds.get_lux(i)

            if min_lux is not None and max_lux is not None:
                if lux < min_lux:
                    min_lux = lux
                elif lux > max_lux:
                    max_lux = lux
            else:
                min_lux = lux
                max_lux = lux

        for i in range(self.ds.num_samples) :
            lux = self.ds.get_lux(i)

            y = self.calculate_y(lux, min_lux, max_lux)
            self.display.rect(i, y, 1, 1);

        lux = self.ds.get_lux()
        lux_string = f"{int(lux):,}"
        self.display.overlay_text((48, 0), lux_string, font_large=True, align_right=True, rectangle=True)
        spacing = self.display.font.getsize(lux_string)[1] + 1
        if min_lux is not None and max_lux is not None:
            range_string = f"{int(min_lux):,}-{int(max_lux):,}"
        else:
            range_string = "------"
        self.display.overlay_text((48, 0 + spacing), range_string, font_large=False, align_right=True, rectangle=True)
        lux_icon = Image.open(f"{path}/icons/bulb-light.png")
        self.display.icon((self.margin, 0), lux_icon)

        self.display.update()

    def calculate_y(self, t, min, max):
        """Calculates the y-coordinate on a parabolic curve, given x."""
        delta = (max - min) + 2 
        y = 1 + ((self.display.HEIGHT-20) / (max - min +2)) * (t-min)

        return int(self.display.HEIGHT-y)



