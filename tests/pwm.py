import RPi.GPIO as GPIO
from time import sleep

try:
    ledpin = 12				# PWM pin connected to LED
#    GPIO.cleanup()
    GPIO.setwarnings(True)			#disable warnings
    GPIO.setmode(GPIO.BOARD)		#set pin numbering system
    GPIO.setup(ledpin,GPIO.OUT)
    pi_pwm = GPIO.PWM(ledpin,1000)		#create PWM instance with frequency
    pi_pwm.start(100)				#start PWM of required Duty Cycle 
    while True:
#    for duty in range(0,101,1):
#        pi_pwm.ChangeDutyCycle(duty) #provide duty cycle in the range 0-100
#        sleep(0.01)
#    sleep(0.5)
#    
#    for duty in range(100,-1,-1):
#        pi_pwm.ChangeDutyCycle(duty)
#        sleep(0.01)
#    sleep(0.5)
        pi_pwm.ChangeDutyCycle(100)
        sleep(1)
        pi_pwm.ChangeDutyCycle(0)
        sleep(1)
finally:
    pi_pwm.stop()
    GPIO.cleanup()
