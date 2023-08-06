from collections import defaultdict
from threading import RLock
import traceback
import types

from pandabus.event import StringEvent, EventMeta


_func_db={}
def fixself(func):
    def wrapper(self=None,*arg,**kwarg):
        if self is None:
             return func(**kwarg)
        return func(self,*arg,**kwarg)
    return wrapper    

def _reg_func(raw,func):
    if raw.__module__=="__main__":
        _func_db[raw.__qualname__]=func
    else:
        _func_db[raw.__module__+':'+raw.__qualname__]=func

def fix_func(func):
    if isinstance(func,types.FunctionType):
        return func
    return _func_db[func]

def resolve_run(bus,ent):  # Turbo Sort.
    ent_typ=type(ent)
    ind=defaultdict(int)
    for i,j in bus.afters.items():
        if i[0]!=ent_typ:
            continue
        for k in j:
            ind[k]+=1
    for i in bus.listener[ent_typ]:
        if i not in ind:
            ind[i]=0
    def update(func):
        for i in bus.afters[(ent_typ,func)]:
            ind[i]-=1
    
    while True:
        for i,j in ind.items():
            if j==0:# Can Run
                i(ent)
                update(i)
                ind[i]=-1
                break
        else:
            break
        if ent.canceled:
            break

class Bus():
    singleton={}
    @fixself
    class EventBusListener():
        def __init__(self,bus,func,locks=None):
            self.func=func
            self.bus=bus
            self.locks=locks or []
        def __call__(self,*arg,**kwarg):
            for lock in self.locks:
                self.bus.locks[lock].acquire()
            try:
                res=self.func(*arg,**kwarg)
            finally:
                for lock in self.locks:
                    self.bus.locks[lock].release()
            return res
        @property
        def __name__(self):
            return self.func.__name__
    def __new__(cls,name):
        if name in cls.singleton:
            return cls.singleton[name]
        cls.singleton[name]=object.__new__(cls)
        cls.singleton[name]._init(name)
        return cls.__new__(cls,name)
    def _init(self,name):
        self.name=name
        self.listener=defaultdict(list)
        self.locks=defaultdict(RLock)
        self.afters=defaultdict(list)
        
    @fixself
    class listen(object):
        def __init__(self,bus,name_or_event,before=None,after=None):
            # <before> and <after> will NOT work yet, I were working on it.
            if isinstance(name_or_event,str):
                name_or_event=getattr(StringEvent,name_or_event)
            self.bus=bus
            self.event=name_or_event
            self.locks=[]
            before = before or []
            after = after or []
            if not isinstance(before,list):
                before=[before]
            if not isinstance(after,list):
                after=[after]
            self.before=[]
            self.after=[]
            for i in after:
                self.after.append(fix_func(i))
            for i in before:
                self.before.append(fix_func(i))
        def lock(self,lk):
            self.locks.append(lk)
        def __call__(self,func):
            res=self.bus.EventBusListener(func,self.locks)
            _reg_func(func,res)
            self.bus.listener[self.event].append(res)
            self.bus.afters[(self.event,res)]+=self.before
            for x in self.after:
                self.bus.afters[(self.event,x)].append(res)
            return res
            
    def send(self,name_or_event,*arg):
        if isinstance(name_or_event,str):
            name_or_event=getattr(StringEvent,name_or_event)
        event=name_or_event(*arg)
        resolve_run(self,event)
        """for listener in self.listener[name_or_event]:
            try:
                listener(event)
            except Exception as exc:
                traceback.print_exception(exc)
            if event.canceled:
                break"""
       