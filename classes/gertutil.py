import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir + "/external")

import gertbot as gb

board = 0
d0 = 0
d1 = 0
peltier_channel = 3
led1_channel = 0
led2_channel = 1
inited = 0

def pwm_init (channel) :
   # Set channel for brushed and start motor
   global inited
   if inited == 0 :
       gb.open_uart(0)
       version = gb.get_version(board)
       print("Board version {}".format(version))
       inited = 1

   gb.set_mode(board,channel,gb.MODE_BRUSH)
   gb.move_brushed(board,channel,gb.MOVE_B)

def pwm_set (channel,freq,dc) :
   gb.read_error_status(board)
   gb.pwm_brushed(board,channel,freq,dc)

def pwm_off (channel) :
   gb.set_mode(board,channel,gb.MODE_OFF)

def opendrain_set(d,on) :
   global d0
   global d1
   global inited

   if inited == 0:
       gb.open_uart(0)
       version = gb.get_version(board)
       print("Board version {}".format(version))
       inited = 1

   if d == 0 :
      d0 = on
   elif d == 1 :
      d1 = on

   gb.activate_opendrain(board,d0,d1);

