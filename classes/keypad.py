import RPi.GPIO as GPIO

class Keypad:

    def __init__ (self) :
        print("[KEYP] Initialized")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def upPressed (self) :
        if (GPIO.input(21)) :
            print("[KEYP] UP")

        return GPIO.input(21)

    def downPressed (self) :
        if (GPIO.input(16)) :
            print("[KEYP] DOWN")

        return GPIO.input(16)

    def leftPressed (self) :
        if (GPIO.input(26)) :
            print("[KEYP] LEFT")

        return GPIO.input(26)

    def rightPressed (self) :
        if (GPIO.input(20)) :
            print("[KEYP] RIGHT")

        return GPIO.input(20)


