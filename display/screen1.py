class Screen1 :
    def __init__ (self,d) :
       print("[SCR1] Initialized\n")
       self.display = d

    def update (self, ds) :
       self.display.drawInit()
       self.display.text((0,0), "{}".format(ds.get_humidity()))
       self.display.update()
