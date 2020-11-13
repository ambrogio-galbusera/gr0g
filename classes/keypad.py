from gpiozero import Button

class Keypad:

    def __init__ (self) :
        print("[KEYP] Initialized")
        self.up = Button(0)
        self.down = Button(1)
        self.left = Button(2)
        self.right = Button(3)

    def upPressed (self) :
        if (self.up.is_pressed) :
            print("[KEYP] UP")

        return self.up.is_pressed

    def downPressed (self) :
        if (self.down.is_pressed) :
            print("[KEYP] DOWN")

        return self.down.is_pressed

    def leftPressed (self) :
        if (self.left.is_pressed) :
            print("[KEYP] LEFT")

        return self.left.is_pressed

    def rightPressed (self) :
        if (self.right.is_pressed) :
            print("[KEYP] RIGHT")

        return self.right.is_pressed


