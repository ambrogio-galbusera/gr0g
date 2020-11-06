from display import Display
from screen1 import Screen1
from keypad import Keypad
from datastore import DataStore

k = Keypad()
ds = DataStore()
ds.add_humidity(10)
print(ds.get_humidity())
d = Display();
s = Screen1(d)
s.update(ds)
print(k.leftPressed())
