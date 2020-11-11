import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir + "/classes")

from datastore import DataStore
from display import Display
from screen1 import Screen1
from keypad import Keypad

k = Keypad()
ds = DataStore()
ds.add_humidity(10)
print(ds.get_humidity())
d = Display();
s = Screen1(d,ds)
s.update()
print(k.leftPressed())
