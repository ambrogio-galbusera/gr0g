import gertutil as gu

class Compressor:
    comp_channel = 0

    def __init__ (self) :
        print("[COMP] opendrain on board {}, channel {}\n".format(gu.board, self.comp_channel))

    def on (self) :
        print("[COMP] Setting on\n")
        gu.opendrain_set(self.comp_channel, 1)

    def off (self) :
        print("[COMP] Setting off\n")
        gu.opendrain_set(self.comp_channel, 0)

