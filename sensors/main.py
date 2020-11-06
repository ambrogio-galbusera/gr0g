from datastore import DataStore
from sensors import Sensors

s = Sensors()
ds = DataStore()
ds.add_humidity(s.humidity())
print(ds.get_humidity())
