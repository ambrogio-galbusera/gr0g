from gpiozero import Button

class Keypad:

    def __init__ (self) :
        print("[KEYP] Initialized")
        self.up = Button(0)
        self.down = Button(1)
        self.left = Button(2)
        self.right = Button(3)

    def upPressed (self) :
        print("[KEYP] UP?")
        return self.up.is_pressed

    def downPressed (self) :
        print("[KEYP] DOWN?")
        return self.down.is_pressed

    def leftPressed (self) :
        print("[KEYP] LEFT?")
        return self.left.is_pressed

    def rightPressed (self) :
        print("[KEYP] RIGHT?")
        return self.right.is_pressed


