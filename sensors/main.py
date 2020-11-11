import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir + "/classes")

from datastore import DataStore
from sensors import Sensors

s = Sensors()
ds = DataStore()
ds.add_humidity(s.humidity())
print(ds.get_humidity())
