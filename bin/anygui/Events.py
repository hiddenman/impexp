
TODO = '''
    - Fix optional arguments/use of kwdargs in place of positionals etc.
'''

__all__ = '''

    any
    link
    unlink
    send
    sender
    caller
    unlinkSource
    unlinkHandler
    unlinkMethods

'''.split()


import time
from References import ref, mapping
registry = mapping()
from Utils import IdentityStack, Bunch
source_stack = IdentityStack()

class Internal: pass
any  = Internal()

class Event(Bunch): pass

#def link(source, event, handler,  weak=0, loop=0):
def link(*args, **kwds):
    'Link a source and event to an event handler.'
    assert len(args) < 4, 'link takes only three positional arguments'
    if len(args) == 2:
        source, handler = args; event = 'default'
    else:
        source, event, handler = args
    weak = kwds.get('weak', 0)
    loop = kwds.get('loop', 0)
    s = ref(source, weak)
    h = ref(handler, weak)
    h.loop = loop
    if not registry.has_key(s):
        registry[s] = {}
    if not registry[s].has_key(event):
        registry[s][event] = []
    if not h in registry[s][event]:
        registry[s][event].append(h)
    prodder = getattr(source, 'enableEvent', None)
    if callable(prodder): prodder(event)

#def unlink(source, event, handler):
def unlink(*args, **kwds):
    'Unlink an event handler from a source and event.'
    assert len(args) < 4, 'link takes only three positional arguments'
    if len(args) == 2:
        source, handler = args; event = 'default'
    else:
        source, event, handler = args
    h = ref(handler, weak=0)
    for lst in lookup(source, event):
        try:
            lst.remove(h)
        except (KeyError, ValueError): pass

def lookup(source, event):
    source = ref(source, weak=0)
    lists = []
    sources = [source]
    if source() is not any: sources.append(ref(any, weak=0))
    events = [event]
    if event is not any: events.append(any)
    for s in sources:
        for e in events:
            try:
                h = registry[s][e]
                lists.append(registry[s][e])
            except KeyError: pass
    return lists

def send(source, event='default', loop=0, **kw):
    'Call the appropriate event handlers with the supplied arguments. \
    As a side-effect, dead handlers are removed from the candidate lists.'
    args = {'source': source, 'event': event, 'time': time.time()}
    args.update(kw)
    args.setdefault('dict', args)
    source_stack.append(source)
    try:
        results = []
        for handlers in lookup(source, event):
            live_handlers = []
            for r in handlers:
                if not r.is_dead():
                    live_handlers.append(r)
                    obj = r.obj
                    if obj is not None:
                        obj = obj()
                        if not loop and not r.loop \
                           and obj in source_stack: continue
                    handler = r()
                    result = handler(Event(**args))
                    if result is not None: results.append(result)
            handlers[:] = live_handlers
        if results: return results
    finally:
        source_stack.pop()

class Sender:
    def __init__(self, event='default'):
        self.event = event
    def __call__(self, event):
        args = event.dict.copy()
        del args['source']
        del args['event']
        send(event.source, self.event, **args)
        
sender = Sender

class Caller:
    def __init__(self, func, args, kwds):
        self.func = func
        self.args = args
        self.kwds = kwds
    def __call__(self, *args, **kwds):
        return self.func(*self.args, **self.kwds)

caller = Caller

class DefaultEventMixin:

    def __init__(self):
        if hasattr(self, '_defaultEvent'):
            link(self, self._defaultEvent, self._defaultEventHandler,
                 weak=1, loop=1)

    def _defaultEventHandler(self, event):
        args = event.dict.copy()
        del args['source']
        del args['event']
        send(self, 'default', **args)
                         
def unlinkSource(source):
    'Unlink all handlers linked to a given source.'
    del registry[source]

def unlinkHandler(handler):
    'Unlink a handler from the event framework.'
    h = ref(handler, weak=0)
    for s in registry.keys():
        for e in registry[s].keys():
            try: retistry[s][e].remove(h)
            except ValueError: pass

def unlinkMethods(obj):
    'Unlink all the methods of obj that are handlers.'
    for name in dir(obj):
        attr = getattr(obj, name)
        if callable(attr):
            try:
                unlinkHandler(attr)
            except: pass
