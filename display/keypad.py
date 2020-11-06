from gpiozero import Button

class Keypad:

    def __init__ (self) :
        print("[KEYP] Initialized\n")
        self.up = Button(0)
        self.down = Button(1)
        self.left = Button(2)

    def upPressed (self) :
        print("[KEYP] UP?\n")
        return self.up.is_pressed

    def downPressed (self) :
        print("[KEYP] DOWN?\n")
        return self.down.is_pressed

    def leftPressed (self) :
        print("[KEYP] LEFT?\n")
        return self.left.is_pressed

