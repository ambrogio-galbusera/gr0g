import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir + "/classes")

import time
import gertutil as gu

gu.pwm_init(0)
gu.pwm_init(2)
while (True) :
    gu.pwm_set(0,100,100);
    gu.pwm_set(2,1000,100)
    time.sleep(1)
    gu.pwm_set(2,1000,100);
    time.sleep(1)
