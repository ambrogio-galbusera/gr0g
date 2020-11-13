class AppSettings :
    # in minutes
    dayDuration = 4
    nightDuration = 1

    # in seconds
    sprayPeriod = 600
    sprayTime = 10

    temperatureSetpoint = 25
    humiditySetpoint = 80

    def __init__ (self) :
        self.load()

    def load (self) :
        try:
            file = open('settings.txt', 'r')
            lines = file.readlines()

            count = 0
            # Strips the newline character
            for line in Lines:
                if (count == 0) :
                    self.dayDuration = int(line.strip())
                elif (count == 1) :
                    self.nightDuration = int(line.strip())
                elif (count == 2) :
                    self.sprayPeriod = int(line.strip())
                elif (count == 3) :
                    self.sprayTime= int(line.strip())
                elif (count == 4) :
                    self.temperatureSetpoint = int(line.strip())
                elif (count == 5) :
                    self.humiditySetpoint = int(line.strip())

                count = count + 1
        except:
            print("[APPS] Exception");

    def save (self) :
        try:
            lines = [ "{}\n".format(self.dayDuration),
                      "{}\n".format(self.dayDuration),
                      "{}\n".format(self.nighDuration),
                      "{}\n".format(self.sprayPeriod),
                      "{}\n".format(self.sprayTime),
                      "{}\n".format(self.temperatureSetpoint),
                      "{}\n".format(self.humiditySetpoint) ]

            file = open('settings.txt', 'w')
            file.writelines(L)
            file.close()
        except:
            print("[APPS] Exception")
