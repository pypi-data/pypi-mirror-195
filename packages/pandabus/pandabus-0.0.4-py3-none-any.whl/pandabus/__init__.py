from pandabus.event import Event
from pandabus.bus import Bus


bus = Bus("")
class buses():
    def __getattr__(self,name):
        return Bus(name)
buses = buses()

