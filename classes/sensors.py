
try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

from bme280 import BME280


class Sensors:
    # BME280 temperature/pressure/humidity sensor
    bme280 = BME280()

    def __init__ (self) :
        print("[SENS] Initializing\n")

    def humidity (self) :
        h = self.bme280.get_humidity()
        print("[SENS] Humidity: {}\n".format(h))
        return h


    def temperature (self) :
        t = self.bme280.get_temperature()
        print("[SENS] Temperature: {}\n".format(t))
        return t

    def cpu_temperature (self) :
        process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
        output, _error = process.communicate()
        t = float(output[output.index('=') + 1:output.rindex("'")])
        print("[SENS] CPU Temperature: {}\n".format(t))
        return t

    def lux (self) :
        l = ltr559.get_lux()
        print("[SENS] Lux: {}\n".format(l))
        return l


