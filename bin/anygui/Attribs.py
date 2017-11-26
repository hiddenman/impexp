from __future__ import nested_scopes # Support for 2.1
from Events import link, send
from Utils import getGetter,getSetter,getterName,uncapitalizeAttribute

# DONE: Add mechanism for internal attributes (not in state[]). Uses
# _foo naming convention for now...::
# @@@ use rawDictSet('attr',val) (put attr in __dict__) in subclass __init__
# then attrib.attr will get the right value
# and __setattr__ logic has been changed so that attrib.attr = val
# will do the right thing (check whether attr in __dict__)


# New functionality: if methods set<Attrib> or get<Attrib> are
# present, use them to get or set "attrib". - jak

class Attrib:
    # TODO: Add new docstring (see below for old one)

    def __init__(self, *args, **kwds):
        self._getstack=[]
        defaults = getattr(self, 'state', {})
        self.state = defaults.copy()
        self.set(*args, **kwds)
        # @@@ should this really be here, I think I would be better
        # factored out and be responsability of the subclasses to call this,
        # for examples for proxies it generates a redundant push

    def push(self, *names): pass

    def pull(self,*names): pass

    def rawDictSet(self,name,value):
        self.__dict__[name] = value

    def __setattr__(self, name, value):
        if name == 'state' or name[0] == '_'or self.__dict__.has_key(name):
            self.__dict__[name] = value
        else:
            method = getSetter(self,name)
            if method:
                method(value)
            else:
                self.set(**{name: value})

    def __getattr__(self, name):
        if name[0] == '_': raise AttributeError, name
        if name == 'state':
            raise AttributeError, name
        if name[:3] != 'set' and name[:3] != 'get':
            method = getGetter(self,name)
            if method:
                return method()
        
        # ===== FOR MODELS ===== #
        if name.startswith('install') and name.endswith('Model'):
            def metaInstall(model):
                self.installModel(self, uncapitalizeAttribute(name[7:-5]), model)
            return metaInstall
        if name.startswith('remove') and name.endswith('Model'):
            def metaRemove():
                self.removeModel(self, uncapitalizeAttribute(name[6:-5]))
            return metaRemove
        # === END FOR MODELS === #

        
        if not self.state.has_key(name):
            raise AttributeError, name
        try:
            # Lazy update.
            if name not in self._getstack:
                self._getstack.append(name)
                try:
                    #print "attrib-pull",name # @@@ debug
                    self.pull(*(name,))
                finally:
                    del self._getstack[-1]
        except (AttributeError,KeyError):
            pass
        #print "attrib-from-state",name # @@@ debug
        return self.state[name]

    def set(self, *args, **kwds):
        names = self.rawSet(*args, **kwds)
        self.push(*names)

    def rawSet(self, *args, **kwds):
        names = []
        for key, val in optsAndKwdsItems(args, kwds):
            #old_val = getattr(self, key, None)
            #try: old_val.removed(self, key)
            #except: pass
            meth = getSetter(self,key)
            if meth:
                meth(val)
            else:
                self.state[key] = val
                #try: val.assigned(self, key)
                #except: pass
                names.append(key)
        return names

    def modify(self, *args, **kwds):
        names = self.rawModify(*args, **kwds)
        self.push(*names)

    def rawModify(self, *args, **kwds):
        names = []
        for key, val in optsAndKwdsItems(args, kwds):
            modattr(self, key, val)
            names.append(key)
        return names


def optsAndKwdsItems(args, kwds):
    items = kwds.items()
    for opt in args:
        items.extend(opt.__dict__.items())
    return items


def modattr(obj, name, value):
    old_value = getattr(obj, name, None)
    # try assigning to the "all-object slice"
    try: old_value[:] = value
    except:
        # try assigning to the "value" attribute of the old-value
        try: old_value.value = value
        except:
            # no in-place mod, so, just set it (bind or re-bind)
            # Use rawSet() if available:
            setter = getattr(obj, 'rawSet', None)
            if callable(setter):
                setter(**{name: value})
            else: setattr(obj, name, value)
            return
    # in-place modification has succeeded, alert the old_value (if
    # it supplies a suitable method)
    try: old_value.push()
    except: pass




OLD_DOCSTRING = """Attrib: mix-in class to support attribute getting & setting.


    Each attribute name may have a setter method _set_name and/or a getter
    method _get_name.  If only the latter, it's a read-only attribute.  If
    no _set_name, attribute is set directly in self.__dict__.  This only
    applies to attribute-names that do NOT start with '_'.

    If the value being set exposes a method .assigned, it's called just
    after the attribute assignment; if the previously-set value exposes
    a method .removed, it's called just before the attribute assignment.
    This supports Models as values for widget attributes.

    Besides __setattr__ and __getattr__ special methods with this
    functionality, Attrib supplies a set method to set many attributes
    and options, and an __init__ with similar functionality.  __init__
    also handles attributes listed in self.explicit_attributes.

    Another, similar feature of class Attrib: it supplies a modattr method
    that tries to change an attribute's value in-place, if feasible, rather
    than re-bind it.  Changing in-place means trying _modify_name (rather
    than _set_name), assigning to self.name[:], and assigning to
    self.name.value.  In the end, self.name is re-bound if in-place
    modification fails.  If the value being changed exposes a method
    .modified, it's called just after an in-place modification succeeds.

    Method modify has the same interface as set (to modify potentially
    more than one attribute at once) but uses modattr rather than setattr.

    Attrib also supplies a default sync method, which calls all the
    relevant methods named set* in the connected _dependant object if
    flag _inhibit_sync is false.  In this release, all set* are
    called; eventually, some kind of mechanism will use the hints to
    be more selective/optimizing.  Attrib's responsibilities include
    enforcing a calling order among set* methods.


    Note that Attrib embodies two patterns (attribute setting/getting
    and sync functionality) and is thus "Alexandrian dense"; cfr
    Vlissides, "Pattern Hatching", page 30, for pluses and minuses of
    such "dense" approaches and the resulting "profound" code.
    """
