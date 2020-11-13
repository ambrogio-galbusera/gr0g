class DataStore:

    num_samples = 160

    def __init__ (self) :
        print("[DS  ] Initialized")
        self.humis = [0] * self.num_samples
        self.temps = [0] * self.num_samples
        self.raw_temps = [0] * self.num_samples
        self.luxs = [0] * self.num_samples
        self.cpu_temps = [0] * 5
        self.factor = 2.25

    def add_humidity (self, value) :
        corr_humidity = self.correct_humidity(value, self.raw_temps[self.num_samples-1], self.temps[self.num_samples-1])
        print("[DS  ] Adding humidity: {} -> {}".format(value, corr_humidity))
        self.humis = self.humis[1:] + [corr_humidity]

    def get_humidity (self, idx=-1) :
        if idx == -1 :
            idx = self.num_samples-1

        t = self.humis[idx];
        print("[DS  ] Reading humidity: {}".format(t))
        return t

    def add_temperature (self, value) :
        # Corrected temperature
        avg_cpu_temp = sum(self.cpu_temps) / float(len(self.cpu_temps))
        corr_temperature = value - ((avg_cpu_temp - value) / self.factor)

        print("[DS  ] Adding temperature: {} -> {}".format(value, corr_temperature))
        self.raw_temps = self.raw_temps[1:] + [value]
        self.temps = self.temps[1:] + [corr_temperature]

    def get_temperature (self, idx=-1) :
        if idx == -1 :
            idx = self.num_samples-1

        t = self.temps[idx];
        print("[DS  ] Reading temperature: {}".format(t))
        return t

    def add_lux (self, value) :
        print("[DS  ] Adding lux: {}".format(value))
        self.luxs = self.luxs[1:] + [value]

    def get_lux (self, idx=-1) :
        if idx == -1 :
            idx = self.num_samples-1

        t = self.luxs[idx];
        print("[DS  ] Reading lux: {}".format(t))
        return t

    def add_cpu_temperature (self, value) :
        print("[DS  ] Adding CPU temperature: {}".format(value))
        self.cpu_temps = self.cpu_temps[1:] + [value]

    def get_cpu_temperature (self) :
        t = self.cpu_temps[4];
        print("[DS  ] Reading CPU temperature: {}".format(t))
        return t

    def correct_humidity(self, humidity, temperature, corr_temperature):
        dewpoint = temperature - ((100 - humidity) / 5)
        corr_humidity = 100 - (5 * (corr_temperature - dewpoint))
        return min(100, corr_humidity)

