import os
import time
import colorsys
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class ScreenHumidityGraph :
    # Margins
    margin = 3

    def __init__ (self,d,ds,sett,kp) :
        print("[HUMG] Initialized")
        self.display = d
        self.ds = ds
        self.sett = sett
        self.keypad = kp

    def process (self) :
        return (self.keypad.leftPressed() or self.keypad.rightPressed())

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
        self.display.overlay_text((68, 0), humidity_string, font_size=2, align_right=True, rectangle=True)
        humidity_icon = Image.open(f"{path}/icons/humidity.png")
        self.display.icon((self.margin, 0), humidity_icon)

        self.display.update()

    def calculate_y(self, t, min, max):
        """Calculates the y-coordinate on a parabolic curve, given x."""
        delta = (max - min) + 2 
        y = 1 + ((self.display.HEIGHT-20) / (max - min +2)) * (t-min)

        return int(self.display.HEIGHT-y)



