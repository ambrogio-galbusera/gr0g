
import time,sys
import datetime
import gertbot as gb

board = 0
d0 = 0
d1 = 0
fan_channel = 0
fan_freq = 1000
peltier_channel = 1
led1_channel = 2
led2_channel = 3

def pwm_init (channel) :
   # Set channel for brushed and start motor
   gb.set_mode(board,channel,gb.MODE_BRUSH)
   gb.move_brushed(board,channel,gb.MOVE_B)

def pwm_set (channel,freq,dc) :
   gb.pwm_brushed(board,channel,freq,dc)

def pwm_off (channel) :
   gb.set_mode(board,channel,gb.MODE_OFF)

def opendrain_set(d,on) :
   global d0
   global d1

   if d == 0 :
      d0 = on
   elif d == 1 :
      d1 = on

   gb.activate_opendrain(board,d0,d1);

########
#
# Fan PWM
#
########
def fan_init () :
   print("[FAN] PWM brushed on board {}, channel {}\n".format(board, fan_channel))
   pwm_init(fan_channel)
   pwm_set(fan_channel,fan_freq,0)

def fan_set (dc) :
   print("[FAN] Setting PWM to {}\n".format(dc))
   pwm_set(fan_channel,fan_freq,dc)

def fan_off () :
   print("[FAN] Power off\n")
   pwm_off(fan_channel)
########


########
#
# COMPRESSOR
#
########
def compressor_on () :
   opendrain_set(0,1)

def compressor_off () :
   opendrain_set(0,0)

###########################################
# MAIN FUNCTION
###########################################
gb.open_uart(0)
compressor_on()
fan_init()

fan_set(30)
time.sleep(3)

fan_set(100)
time.sleep(3)

fan_set(50)
time.sleep(3)

fan_off()
compressor_off()

