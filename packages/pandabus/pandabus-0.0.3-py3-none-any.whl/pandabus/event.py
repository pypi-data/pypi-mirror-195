from dataclasses import dataclass,_DataclassParams


class EventMeta(type):
    singleton={}
    def __new__(cls,name,bases,dict,static=False,cancelable=False):
        if name in cls.singleton:
            return cls.singleton[name]
        def cancel(self):
            self.canceled=True
        dict["canceled"]=False
        if cancelable:
            dict["cancel"]=cancel
        res=type.__new__(cls,name,bases,dict)
        if res.__module__=="simpleeventbus.event" and name=="Event":
            return res
        res=dataclass(res,frozen=static)
        cls.singleton[name]=res
        return res


class Event(metaclass=EventMeta):
    pass
    
class StringEvent():
    def __getattr__(self,name):
        return EventMeta.__new__(EventMeta,name,(Event,),{})

StringEvent = StringEvent()
