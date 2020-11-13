import gertutil as gu

class Compressor:
    comp_channel = 0

    def __init__ (self) :
        print("[COMP] opendrain on board {}, channel {}".format(gu.board, self.comp_channel))

    def on (self) :
        print("[COMP] Setting on")
        gu.opendrain_set(self.comp_channel, 1)

    def off (self) :
        print("[COMP] Setting off")
        gu.opendrain_set(self.comp_channel, 0)

