import os
import time
import pytz
import colorsys
from pytz import timezone
from astral.geocoder import database, lookup
from astral.sun import sun
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class Screen1 :
    # The city and timezone that you want to display.
    city_name = "Sheffield"
    time_zone = "Europe/London"

    # Values that alter the look of the background
    blur = 50
    opacity = 125

    mid_hue = 0
    day_hue = 25

    sun_radius = 50

    # Margins
    margin = 3

    def __init__ (self,d,ds) :
       print("[SCR1] Initialized\n")
       self.display = d
       self.ds = ds
       self.start_time = time.time()
       self.cpu_temps = [self.ds.get_cpu_temperature()] * 5
       self.factor = 2.25
       self.min_temp = None
       self.max_temp = None

    def update (self) :
        self.display.drawInit()

        path = os.path.dirname(os.path.realpath(__file__))
        progress, period, day, local_dt = self.sun_moon_time(self.city_name, self.time_zone)
        background = self.draw_background(progress, period, day)

        # Temperature
        temperature = self.ds.get_temperature()

        # Corrected temperature
        cpu_temp = self.ds.get_cpu_temperature()
        self.cpu_temps = self.cpu_temps[1:] + [cpu_temp]
        avg_cpu_temp = sum(self.cpu_temps) / float(len(self.cpu_temps))
        corr_temperature = temperature - ((avg_cpu_temp - temperature) / self.factor)

        time_elapsed = time.time() - self.start_time
        if time_elapsed > 30:
           if self.min_temp is not None and self.max_temp is not None:
               if corr_temperature < self.min_temp:
                   self.min_temp = corr_temperature
               elif corr_temperature > self.max_temp:
                   self.max_temp = corr_temperature
           else:
               self.min_temp = corr_temperature
               self.max_temp = corr_temperature

        temp_string = f"{corr_temperature:.0f}°C"
        self.display.overlay_text((68, 18), temp_string, font_large=True, align_right=True)
        spacing = self.display.font.getsize(temp_string)[1] + 1
        if self.min_temp is not None and self.max_temp is not None:
            range_string = f"{self.min_temp:.0f}-{self.max_temp:.0f}"
        else:
            range_string = "------"
        self.display.overlay_text((68, 18 + spacing), range_string, font_large=False, align_right=True, rectangle=True)
        temp_icon = Image.open(f"{path}/icons/temperature.png")
        self.display.icon((self.margin, 18), temp_icon)

        # Humidity
        humidity = self.ds.get_humidity()
        corr_humidity = self.correct_humidity(humidity, temperature, corr_temperature)
        humidity_string = f"{corr_humidity:.0f}%"
        self.display.overlay_text((68, 48), humidity_string, font_large=True, align_right=True)
        humidity_icon = Image.open(f"{path}/icons/humidity.png")
        self.display.icon((self.margin, 48), humidity_icon)

        # Light
        light = self.ds.get_lux()
        light_string = f"{int(light):,}"
        self.display.overlay_text((self.display.WIDTH - self.margin, 18), light_string, font_large=True, align_right=True)
        light_icon = Image.open(f"{path}/icons/bulb-light.png")
        self.display.icon((80, 18), light_icon)

        self.display.update()

    def correct_humidity(self, humidity, temperature, corr_temperature):
        dewpoint = temperature - ((100 - humidity) / 5)
        corr_humidity = 100 - (5 * (corr_temperature - dewpoint))
        return min(100, corr_humidity)

    def x_from_sun_moon_time(self, progress, period, x_range):
        """Recalculate/rescale an amount of progress through a time period."""

        x = int((progress / period) * x_range)
        return x

    def sun_moon_time(self, city_name, time_zone):
        """Calculate the progress through the current sun/moon period (i.e day or
           night) from the last sunrise or sunset, given a datetime object 't'."""

        city = lookup(city_name, database())

        # Datetime objects for yesterday, today, tomorrow
        utc = pytz.utc
        utc_dt = datetime.now(tz=utc)
        local_dt = utc_dt.astimezone(pytz.timezone(time_zone))
        today = local_dt.date()
        yesterday = today - timedelta(1)
        tomorrow = today + timedelta(1)

        # Sun objects for yesterday, today, tomorrow
        sun_yesterday = sun(city.observer, date=yesterday)
        sun_today = sun(city.observer, date=today)
        sun_tomorrow = sun(city.observer, date=tomorrow)

        # Work out sunset yesterday, sunrise/sunset today, and sunrise tomorrow
        sunset_yesterday = sun_yesterday["sunset"]
        sunrise_today = sun_today["sunrise"]
        sunset_today = sun_today["sunset"]
        sunrise_tomorrow = sun_tomorrow["sunrise"]

        # Work out lengths of day or night period and progress through period
        if sunrise_today < local_dt < sunset_today:
            day = True
            period = sunset_today - sunrise_today
            # mid = sunrise_today + (period / 2)
            progress = local_dt - sunrise_today

        elif local_dt > sunset_today:
            day = False
            period = sunrise_tomorrow - sunset_today
            # mid = sunset_today + (period / 2)
            progress = local_dt - sunset_today

        else:
            day = False
            period = sunrise_today - sunset_yesterday
            # mid = sunset_yesterday + (period / 2)
            progress = local_dt - sunset_yesterday

        # Convert time deltas to seconds
        progress = progress.total_seconds()
        period = period.total_seconds()

        return (progress, period, day, local_dt)

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


