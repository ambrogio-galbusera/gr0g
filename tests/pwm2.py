import os
import time

os.system("echo 0 > /sys/class/pwm/pwmchip0/export")
os.system("echo 1000000 > /sys/class/pwm/pwmchip0/pwm0/period")
os.system("echo 0 > /sys/class/pwm/pwmchip0/pwm0/duty_cycle")
os.system("echo 1 > /sys/class/pwm/pwmchip0/pwm0/enable")

time.sleep(10)

try:
    while True :
        for dc in range(0,1000001,10000):
            #os.system("echo 0 > /sys/class/pwm/pwmchip0/pwm0/enable")
            os.system("echo {} > /sys/class/pwm/pwmchip0/pwm0/duty_cycle".format(dc))
            os.system("echo 1 > /sys/class/pwm/pwmchip0/pwm0/enable")

            print("DC {}".format(dc));
            time.sleep(0.1)

        for dc in range(1000000,-1,-10000):
            #os.system("echo 0 > /sys/class/pwm/pwmchip0/pwm0/enable")
            os.system("echo {} > /sys/class/pwm/pwmchip0/pwm0/duty_cycle".format(dc))
            os.system("echo 1 > /sys/class/pwm/pwmchip0/pwm0/enable")

            print("DC {}".format(dc));
            time.sleep(0.1)
  
finally:
    os.system("echo 0 > /sys/class/pwm/pwmchip0/pwm0/enable")
    os.system("echo 0 > /sys/class/pwm/pwmchip0/unexport")


