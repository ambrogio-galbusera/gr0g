import os
import time

def rpwm_init () :
    os.system("echo 0 > /sys/class/pwm/pwmchip0/pwm0/enable")
    os.system("echo 0 > /sys/class/pwm/pwmchip0/unexport")

    os.system("echo 0 > /sys/class/pwm/pwmchip0/export")
    os.system("echo 1000000 > /sys/class/pwm/pwmchip0/pwm0/period")
    os.system("echo 0 > /sys/class/pwm/pwmchip0/pwm0/duty_cycle")
    os.system("echo 1 > /sys/class/pwm/pwmchip0/pwm0/enable")

def rpwm_set (dc) :
    pdc = int(1000000 * dc / 100)
    #os.system("echo 0 > /sys/class/pwm/pwmchip0/pwm0/enable")
    os.system("echo {} > /sys/class/pwm/pwmchip0/pwm0/duty_cycle".format(pdc))
    os.system("echo 1 > /sys/class/pwm/pwmchip0/pwm0/enable")


