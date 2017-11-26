from anygui.Proxies import Proxy
from anygui.Events import DefaultEventMixin
from anygui.Exceptions import SyncError
from anygui.LayoutManagers import LayoutData
from anygui.Rectangles import Rectangle
#from anygui.Rules import RectEngine

#rules = RectEngine()
#rules = RuleEngine()
#rules.define('position = x, y')
#rules.define('size = width, height')
#rules.define('geometry = x, y, width, height')

class Component(Proxy, DefaultEventMixin, Rectangle):    
    """
    Component is an abstract base class representing a visual
    component of the graphical user interface. A Component owns a
    rectangular region of screen space defined by its x, y, width and
    height properties.  It may be contained within another Component.
    """

    #_aggregates = {
    #    'position': ('x', 'y'),
    #    'size': ('width', 'height'),
    #    'geometry': ('x', 'y', 'width', 'height')
    #    }
    
    def __init__(self, *args, **kw):
        DefaultEventMixin.__init__(self)
        Proxy.__init__(self, *args, **kw)

    #def internalSync(self, names):
    #    """
    #    Used to synchronize the aliased attributes.
    #
    #    The attributes handled and the relationships between them:
    #
    #       # Pseudocode; the sequence types need not match:
    #       position == x, y
    #       size     == width, height
    #       geometry == position + size
    #
    #    If the equations above are satisfied, no action is taken. If
    #    one is broken, the parameter 'names' (a sequence of names of
    #    the attributes that may have changed since the last internal
    #    sync) should include only attribute names on one side of the
    #    broken equation, and should include all the attributes that
    #    don't match the other side of the equation. For instance, if
    #    position is (3, 4), x = 2, and y is 4, names should include
    #    either 'position' or 'x', but not both. If it includes 'x', it
    #    may also include 'y', but that doesn't affect the sync. If
    #    these requirements are broken, a SyncError is raised.
    #    """
    #    rules.sync(self, names)

    #def blockedNames(self):
    #    """
    #    Blocks all aggregates from being passed to the backend.
    #    """
    #    return ['position', 'size', 'geometry']

    #def expandAliasedName(self,names,name):
    #    """
    #    Expands an aliased attribute into its aliases, and adds
    #    the aliases to names.
    #    """
    #    for n in rules.atoms: names.append(n)

