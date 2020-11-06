class DataStore:

    def __init__ (self) :
        print("[DS  ] Initialized\n")
        self.humis = [0] * 5
        self.temps = [0] * 5
        self.luxs = [0] * 5
        self.cpu_temps = [0] * 5

    def add_humidity (self, value) :
        print("[DS  ] Adding humidity: {}\n".format(value))
        self.humis = self.humis[1:] + [value]

    def get_humidity (self) :
        t = self.humis[4];
        print("[DS  ] Reading humidity: {}\n".format(t))
        return t

    def add_temperature (self, value) :
        print("[DS  ] Adding temperature: {}\n".format(value))
        self.temps = self.temps[1:] + [value]

    def get_temperature (self) :
        t = self.temps[4];
        print("[DS  ] Reading temperature: {}\n".format(t))
        return t

    def add_lux (self, value) :
        print("[DS  ] Adding lux: {}\n".format(value))
        self.luxs = self.luxs[1:] + [value]

    def get_lux (self) :
        t = self.luxs[4];
        print("[DS  ] Reading lux: {}\n".format(t))
        return t

    def add_cpu_temperature (self, value) :
        print("[DS  ] Adding CPU temperature: {}\n".format(value))
        self.cpu_temps = self.cpu_temps[1:] + [value]

    def get_cpu_temperature (self) :
        t = self.cpu_temps[4];
        print("[DS  ] Reading CPU temperature: {}\n".format(t))
        return t


