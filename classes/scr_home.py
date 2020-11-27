import os
import time
import colorsys
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class ScreenHome :
    # Values that alter the look of the background
    blur = 50
    opacity = 125

    mid_hue = 0
    day_hue = 25

    sun_radius = 50

    # Margins
    margin = 3

    def __init__ (self,d,ds,sett,kp) :
        print("[HOME] Initialized")
        self.display = d
        self.ds = ds
        self.sett = sett
        self.keypad = kp
        self.start_time = time.time()
        self.cpu_temps = [self.ds.get_cpu_temperature()] * 5
        self.factor = 2.25
        self.min_temp = None
        self.max_temp = None
        self.is_night = False
        self.start_day = time.time()
        self.start_night = None

    def process (self) :
        return (self.keypad.rightPressed() or self.keypad.leftPressed())

    def update (self) :
        self.display.drawInit()

        path = os.path.dirname(os.path.realpath(__file__))
        progress, period, day = self.sun_moon_time()
        background = self.draw_background(progress, period, day)
        self.display.background(background)

        # Temperature
        temperature = self.ds.get_temperature()

        time_elapsed = time.time() - self.start_time
        if time_elapsed > 30:
           if self.min_temp is not None and self.max_temp is not None:
               if temperature < self.min_temp:
                   self.min_temp = temperature
               elif temperature > self.max_temp:
                   self.max_temp = temperature
           else:
               self.min_temp = temperature
               self.max_temp = temperature

        temp_string = f"{temperature:.0f}°C"
        self.display.overlay_text((80, 12), temp_string, font_size=2, align_right=True, rectangle=True)
        spacing = self.display.largefont.getsize(temp_string)[1] + 1
        if self.min_temp is not None and self.max_temp is not None:
            range_string = f"{self.min_temp:.0f}-{self.max_temp:.0f}"
        else:
            range_string = "------"
        self.display.overlay_text((80, 12 + spacing), range_string, font_size=0, align_right=True, rectangle=True)
        temp_icon = Image.open(f"{path}/icons/temperature.png")
        self.display.icon((self.margin, 12), temp_icon)

        # Humidity
        humidity = self.ds.get_humidity()
        humidity_string = f"{humidity:.0f}%"
        self.display.overlay_text((80, 48), humidity_string, font_size=2, align_right=True, rectangle=True)
        humidity_icon = Image.open(f"{path}/icons/humidity.png")
        self.display.icon((self.margin, 48), humidity_icon)

        # Light
        light = self.ds.get_lux()
        light_string = f"{int(light):,}"
        self.display.overlay_text((self.display.WIDTH - self.margin, 12), light_string, font_size=2, align_right=True, rectangle=True)
        light_icon = Image.open(f"{path}/icons/bulb-light.png")
        self.display.icon((90, 12), light_icon)

        self.display.update()

    def x_from_sun_moon_time(self, progress, period, x_range):
        """Recalculate/rescale an amount of progress through a time period."""

        x = int((progress / period) * x_range)
        return x

    def sun_moon_time(self):
        """Calculate the progress through the current sun/moon period (i.e day or
           night) from the last sunrise or sunset, given a datetime object 't'."""

        if (self.is_night) :
            delta = time.time() - self.start_night
            duration = self.sett.nightDuration * 60
            if (delta > duration) :
                self.is_night = False
                self.start_day = time.time()
        else :
            delta = time.time() - self.start_day
            duration = self.sett.dayDuration * 60
            if (delta > duration) :
                self.is_night = True
                self.start_night = time.time()

        if (self.is_night) :
            day = False
            period = self.sett.nightDuration * 60
            progress = time.time() - self.start_night
        else :
            day = True
            period = self.sett.dayDuration * 60
            progress = time.time() - self.start_day

        return (progress, period, day)

    def calculate_y_pos(self, x, centre):
        """Calculates the y-coordinate on a parabolic curve, given x."""
        centre = 80
        y = 1 / centre * (x - centre) ** 2

        return int(y)

    def map_colour(self, x, centre, start_hue, end_hue, day):
        """Given an x coordinate and a centre point, a start and end hue (in degrees),
           and a Boolean for day or night (day is True, night False), calculate a colour
           hue representing the 'colour' of that time of day."""

        start_hue = start_hue / 360  # Rescale to between 0 and 1
        end_hue = end_hue / 360

        sat = 1.0

        # Dim the brightness as you move from the centre to the edges
        val = 1 - (abs(centre - x) / (2 * centre))

        # Ramp up towards centre, then back down
        if x > centre:
            x = (2 * centre) - x

        # Calculate the hue
        hue = start_hue + ((x / centre) * (end_hue - start_hue))

        # At night, move towards purple/blue hues and reverse dimming
        if not day:
            hue = 1 - hue
            val = 1 - val

        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, sat, val)]

        return (r, g, b)

    def circle_coordinates(self, x, y, radius):
        """Calculates the bounds of a circle, given centre and radius."""

        x1 = x - radius  # Left
        x2 = x + radius  # Right
        y1 = y - radius  # Bottom
        y2 = y + radius  # Top

        return (x1, y1, x2, y2)


    def draw_background(self, progress, period, day):
        """Given an amount of progress through the day or night, draw the
           background colour and overlay a blurred sun/moon."""

        # x-coordinate for sun/moon
        x = self.x_from_sun_moon_time(progress, period, self.display.WIDTH)

        # If it's day, then move right to left
        if day:
            x = self.display.WIDTH - x

        # Calculate position on sun/moon's curve
        centre = self.display.WIDTH / 2
        y = self.calculate_y_pos(x, centre)

        # Background colour
        background = self.map_colour(x, 80, self.mid_hue, self.day_hue, day)

        # New image for background colour
        img = Image.new('RGBA', (self.display.WIDTH, self.display.HEIGHT), color=background)
        # draw = ImageDraw.Draw(img)

        # New image for sun/moon overlay
        overlay = Image.new('RGBA', (self.display.WIDTH, self.display.HEIGHT), color=(0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)

        # Draw the sun/moon
        circle = self.circle_coordinates(x, y, self.sun_radius)
        overlay_draw.ellipse(circle, fill=(200, 200, 50, self.opacity))

        # Overlay the sun/moon on the background as an alpha matte
        composite = Image.alpha_composite(img, overlay).filter(ImageFilter.GaussianBlur(radius=self.blur))

        return composite


