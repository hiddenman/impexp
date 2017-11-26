"""Test status:

Missing: test_menu

test_aboutdlg OK
test_backend  OK
test_canvas   NA
test_button   OK
test_checkbox OK
test_combobox OK (Not native though)
test_component NA
test_curses OK
test_defaults OK
test_events OK
test_frame  OK
test_interface NA (Others don't pass either)
test_invisible OK
test_label OK
test_layout OK
test_menu
test_modv1 OK
test_modv2 OK
test_modv3 OK
test_openfiledlg OK   (Some bugs on exit)
test_place OK
test_radiobutton NA   (Can't implement, doesn't work like a toggle button)
test_radiogroup  OK
test_references  OK
test_remove   (Works only the first time)
test_rules  NA
test_shake  OK 
test_tags   NA
test_textarea OK
test_textfield OK
test_window    OK

demo/ttt.py OK
demo/ttt2.py NA (Fails on Tk & wx)
demo/ifs.py  NA (Fails on Tk & wx. Canvas missing)
demo/chmodgui.py OK

"""

#try:
# Import Anygui infrastructure. You shouldn't have to change these.
from anygui.backends import *
from anygui.Applications import AbstractApplication
from anygui.Wrappers import AbstractWrapper
from anygui.Events import *
from anygui import application
# End Anygui imports.

# Import anything needed to access the backend API. This is
# your job!
import pygtk
   
pygtk.require('2.0')
    
import gtk
# End backend API imports.
#except:
#    import traceback
#    traceback.print_exc()

__all__ = '''

  Application
  ButtonWrapper
  WindowWrapper
  LabelWrapper
  TextFieldWrapper
  TextAreaWrapper
  ListBoxWrapper
  RadioButtonWrapper
  CheckBoxWrapper
  MenuWrapper
  MenuCommandWrapper
  MenuCheckWrapper
  MenuSeparatorWrapper
  MenuBarWrapper

'''.split()

class ComponentWrapper(AbstractWrapper):

    def __init__(self, *args, **kwds):

        AbstractWrapper.__init__(self, *args, **kwds)

        # 'container' before everything, then geometry.
        self.setConstraints('container','x','y','width','height')

        # addConstraint(self,before,after) adds a constraint that attribute
        # 'before' must be set before 'after', when both appear in the
        # same push operation. An attempt to set mutually contradictory
        # constraints will result in an exception.
        self.addConstraint('geometry', 'visible')

    def widgetFactory(self,*args,**kws):
        raise NotImplementedError, 'should be implemented by subclasses'

    def enterMainLoop(self): # ...
        if not self.widget: return
        self.widget.show()
        self.proxy.push()

    def destroy(self):
        if self.widget:
            self.widget.destroy()
        self.widget = None

    # getters and setters
    def setContainer(self,container):
        if container is None:
            try:
                self.destroy()
            except:
                pass
            return
        parent = container.wrapper
        if parent is not None:
            self.create()
            cont = parent._getContainer()
            self.widget.unparent()
            if hasattr(cont, 'put'):
                cont.put(self.widget, 0, 0)
            elif hasattr(cont, 'add'):
                cont.add(self.widget)
            self.proxy.push(blocked=['container'])

    def create(self):
        if not self.widget:
            self.widget = self.widgetFactory()
            self.widget.visible = self.proxy.state['visible']
            self.widgetSetUp()

    def setGeometry(self,x,y,width,height):
        if not self.widget: return
        if self.widget.parent and hasattr(self.widget.parent, 'move'):
            self.widget.parent.move(self.widget,
                                    int(x), int(y))
        self.widget.set_uposition(int(x), int(y))

        width = max(int(width),   1)
        height = max(int(height), 1)
        
        self.widget.set_size_request(int(width), int(height))
        return        

    def setVisible(self,visible):
        if not self.widget: return
        if visible:
            self.widget.show()
        else:
            self.widget.hide()

    def setEnabled(self,enabled):
        if not self.widget: return
        self.widget.set_sensitive(int(enabled))

    def setText(self,text):
        if not self.widget: return
#        raise NotImplementedError, 'should be implemented by subclasses'

class LabelWrapper(ComponentWrapper):

    def widgetFactory(self, *args, **kws):
        try:
            label = args[0] or ''
        except:
            label = ''
            
        return gtk.Label(label, *args, **kws)

    def setText(self, text):
        if not self.widget: return
        self.widget.set_text(str(text))

class _ComboBoxWrapper(ComponentWrapper):
    def widgetFactory(self, *args, **kws):
        return gtk.Combo()
    def getSelection(self):
        if not self.widget: return
        return int(self.widget.list.selection[0])
    def setSelection(self, selection):
        if not self.widget: return
        self.widget.list.select_row(int(selection), 0)


class ScrollableListBox(gtk.ScrolledWindow):
    """
    A scrollable list box.  Used by ListBoxWrapper.
    """
    def __init__(self, *args, **kw):
        gtk.ScrolledWindow.__init__(self, *args, **kw)
        self._listbox = gtk.CList()
        self._listbox.show()
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.add_with_viewport(self._listbox)

class ListBoxWrapper(ComponentWrapper):

    connected = 0

    def widgetFactory(self, *args, **kws):
        return ScrollableListBox()

    def setItems(self,items):
        """
        Set the contents of the listbox widget. 'items' is a list of
        strings, or of str()-able objects.
        """
        if not self.widget: return
        self.widget._listbox.clear()
        self._items = items[:]
        for item in items:
            self.widget._listbox.append([str(item)])

    def getItems(self):
        """
        Return ths listbox contents, in order, as a list of strings.
        """
        if not self.widget: return
        items = []
        for i in range(self.widget._listbox.rows):
            items.append(self.widget._listbox.get_text(i, 0))        
        return items

    def setSelection(self,selection):
        """
        Set the selection. 'selection' is an integer indicating the
        item to be selected.
        """
        if not self.widget: return
        self.widget._listbox.select_row(int(selection), 0)

    def getSelection(self):
        """
        Return the selected listbox item index as an integer.
        """
        if not self.widget: return
        listbox = self.widget._listbox
        if listbox.selection:
            return listbox.selection[0]
        else:
            return -1

    def widgetSetUp(self):
        """ Connect ListBox events """
        if not self.connected:
            self.widget._listbox.connect("select_row", self._select)
            self.connected = 1

    def _select(self,*args):
        send(self.proxy,'select')

#class CanvasWrapper(ComponentWrapper):
# Fix me!
#    _twclass = tw.Canvas

class ButtonWrapper(ComponentWrapper):
    """
    Wraps a backend command-button widget - the kind you click
    on to initiate an action, eg "OK", "Cancel", etc.
    """
    connected = 0

    def widgetFactory(self, *args, **kws):
        return gtk.Button(*args, **kws)

    def widgetSetUp(self):
        """
        Register a backend event handler to call self.click when
        the user clicks the button.
        """
        if not self.connected:
            self.widget.connect("clicked", self.clickHandler)
            self.connected = 1

    def setText(self, text):
        if not self.widget: return
        
        if self.widget.get_children():
            self.widget.get_children()[0].set_text(str(text))
        else:
            label = gtk.Label(str(text))
            label.show()
            self.widget.add(label)

    def clickHandler(self,*args,**kws):
        send(self.proxy,'click')

class ToggleButtonMixin(ButtonWrapper):
    def widgetFactory(self, *args, **kws):
        return gtk.ToggleButton(*args, **kws)

    def getOn(self):
        """ Return the button's state: 1 for checked, 0 for not. """
        if not self.widget: return
        return self.widget.get_active()

    def widgetSetUp(self):
        ButtonWrapper.widgetSetUp(self)
        self._toggling = 0
        self.widget.connect('toggled', self.toggleHandler)
        
    def setOn(self,on):
        """ Set the button's state. """
        if not self.widget: return
        val = self.widget.get_active()
        if val == int(on):
            return
        
        self._toggling = 1        
        self.widget.set_active(int(on))
        self._toggling = 0

    def toggleHandler(self, data):
        if not self._toggling:
            send(self.proxy, 'click')
    
    def clickHandler(self, data):        
        if not self._toggling:
            send(self.proxy, 'click')
            

class CheckBoxWrapper(ToggleButtonMixin):
    """
    Usually ToggleButtonMixin completely handles the CheckBox
    behavior, but in case it doesn't, you may need to write some
    code here.
    """
    def widgetFactory(self, *args, **kws):
        return gtk.CheckButton(*args, **kws)
    

class RadioButtonWrapper(ToggleButtonMixin):
    """
    Radio buttons are a pain. Only one member of an RB "group" may be
    active at a time. Anygui provides the RadioGroup front-end
    class, which takes care of querying the state of radiobuttons
    and setting their state in a mutually exclusive manner.
    However, many backends also enforce this mutual exclusion,
    which means that things can get complicated. The RadioGroup
    class is implemented in as non-intrusive a way as possible,
    but it can be a challenge to arrange for them to act in
    the correct way, backend-wise. Look at the other backend
    implementations for some clues.

    In the case where a backend implements radiobuttons as a simple
    visual variant of checkboxes with no mutual-exclusion behavior,
    this class already does everything you need; just create the
    proper backend widget in RadioButtonWrapper.widgetFactory(). You
    can usually fake that kind of backend implementation by playing
    tricks with the backend's mutual-exclusion mechanism. For example,
    create a tiny frame to encapsulate the backend radiobutton, if
    your backend enforces mutual exclusion on a per-frame basis.
    """

    def widgetFactory(self, *args, **kws):
        if self.proxy.group and len(self.proxy.group._items) > 1:
            item = None
            for item in self.proxy.group._items:
                if item is not self:
                   break
            else:
                raise InternalError(self, "Couldn't find non-self group item!")
            return gtk.RadioButton(item.wrapper.widget, *args, **kws)
        else:
            return gtk.RadioButton(None, *args, **kws)

    def setGroup(self,group):
        if group is None:
            return
        if self.proxy not in group._items:
            group._items.append(self.proxy)
            
class TextFieldWrapper(ComponentWrapper):
    """
    Wraps a native single-line entry field.
    """
    def setEditable(self,editable):
        """
        Set the editable state of the widget. If 'editable' is 0,
        the widget should allow selection and copying of its text,
        but should not accept user input.
        """
        if not self.widget: return
        self.widget.set_editable(editable)

    def getSelection(self):
        """
        Return the first and last+1 character indexes covered by the
        selection, as a tuple; or (0,0) if there's no selection.
        """
        if not self.widget: return
        bounds = self.widget.get_selection_bounds()
        if bounds:
            return bounds
        else:
            position = self.widget.get_position()
            return (position, position)

    def setSelection(self,selection):
        """
        Select the indicated text. 'selection' is a tuple of two
        integers indicating the first and last+1 indexes within
        the widget text that should be covered by the selection.
        """
        if not self.widget: return
        self.widget.select_region(selection[0], selection[1])

    def setText(self,text):
        """ Set/get the text associated with the widget. This might be
        window title, frame caption, label text, entry field text,
        or whatever.
        """
        if not self.widget: return
        self.widget.delete_text(0, -1)
        self.widget.insert_text(str(text))

    def getText(self):
        """
        Fetch the widget's associated text. You *must* implement this
        to get the text from the native widget; the default getText()
        from ComponentWrapper (almost) certainly won't work.
        """
        if not self.widget: return
        return self.widget.get_chars(0, -1)
    
    def widgetFactory(self, *args, **kws):
        return gtk.Entry(*args, **kws)
    
    def widgetSetUp(self):
        """
        Arrange for a press of the "Enter" key to call self._return.
        """
        pass

    def _return(self,*args,**kws):
        send(self.proxy, 'enterkey')

class ScrollableTextView(gtk.ScrolledWindow):
    """
    A scrollable text view.  Used by TextAreaWrapper.
    """
    def __init__(self, *args, **kw):
        gtk.ScrolledWindow.__init__(self, *args, **kw)        
        self._textview = gtk.TextView()
        self._textview.show()
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.add(self._textview)

class TextAreaWrapper(ComponentWrapper):
    """
    Wraps a native multiline text area. If TextControlMixin works
    for your backend, you shouldn't need to change anything here.
    """
    def widgetFactory(self, *args, **kws):
        frame = gtk.Frame()
        scrollable = ScrollableTextView(*args, **kws)
        scrollable.show()
        frame.add(scrollable)
        frame._textview = scrollable._textview
        return frame

    def widgetSetUp(self):
        if self.widget:
            self.widget._textview.set_wrap_mode(gtk.WRAP_WORD)
    
    def getText(self):
        if not self.widget: return
        buffer = self.widget._textview.get_buffer()
        return buffer.get_text(buffer.get_start_iter(),
                               buffer.get_end_iter(),
                               False)

    def setText(self, text):
        if not self.widget: return
        self.widget._textview.get_buffer().set_text(str(text))

    def setSelection(self, selection):
        if not self.widget: return
        start, end = selection
        buffer = self.widget._textview.get_buffer()
        buffer.move_mark_by_name('selection_bound',
                                 buffer.get_iter_at_offset(start))
        buffer.move_mark_by_name('insert',
                                 buffer.get_iter_at_offset(end))

    def getSelection(self):
        return self.widget._textview.get_selection_bounds()

    def setEditable(self, editable):
        if not self.widget: return
        self.widget._textview.set_editable(editable)        


# Incomplete: fix the remainder of this file!

class ContainerMixin:
    """
    Frames - that is, widgets whose job is to visually group
    other widgets - often have a lot of behavior in common
    with top-level windows. Abstract that behavior here.
    """
    pass

class FrameWrapper(ContainerMixin,ComponentWrapper):

    def __init__(self,*args,**kws):
        ComponentWrapper.__init__(self,*args,**kws)

    def widgetFactory(self):
        return gtk.Frame()
    
    def _getContainer(self):
        if not hasattr(self, '_gtk_container'):
            self.create()

        return self._gtk_container

    def widgetSetUp(self):
        if not hasattr(self, '_gtk_container'):
            self._gtk_container = gtk.Layout()
            self.widget.add(self._gtk_container)
            self._gtk_container.show()

    def addToContainer(self,container):
        """
        Add the Frame to its back-end container (another
        Frame or a Window).
        """
        #container.wrapper.widget.add(self.widget)
        raise NotImplementedError, 'should be implemented by subclasses'

    def setContainer(self, *args, **kws):
        """
        OK, this probably needs to be pulled into a mixin heritable by
        various backends.
        
        Ensure all contents are properly created. This looks like it could
        be handled at the Proxy level, but it probably *shouldn't* be -
        it's handling a Tk-specific requirement about the order in which
        widgets must be created. (I did it the Proxy way too. This way
        is definitely "the simplest thing that could possibly work.") - jak
        """
        ComponentWrapper.setContainer(self, *args, **kws)
#        for component in self.proxy.contents:
#            component.container = self.proxy
    
    

class WindowWrapper(ContainerMixin,ComponentWrapper):
    """
    Wraps a top-level window frame.
    """
    connected = 0

    def widgetFactory(self, *args, **kws):
        return gtk.Window(gtk.WINDOW_TOPLEVEL)

    def setTitle(self,title):
        if not self.widget: return
        self.widget.set_title(str(title))

    def _getContainer(self):
        if not hasattr(self, '_gtk_container'):
            self.widgetSetUp()
        return self._gtk_container
    
    def addToContainer(self,container):
        """
        Add self to the backend application, if required.
        """
        raise NotImplementedError, 'should be implemented by subclasses'

    def widgetSetUp(self):
        """
        Arrange for self.resize() to be called whenever the user
        interactively resizes the window.
        """
        if not self.widget:
            self.create()

        if not hasattr(self, '_gtk_container'):
            self._gtk_container = gtk.Layout()
            self.widget.add(self._gtk_container)
            self._gtk_container.show()
        if not self.connected:
            self.widget.connect('size_allocate', self.resizeHandler)
            self.widget.connect('destroy', self.close)
            self.connected = 1

    def close(self, event):
        self.widget.destroy()
        self.destroy()
        application().remove(self.proxy)

    def resizeHandler(self, *args):
        w = self.widget.get_allocation().width
        h = self.widget.get_allocation().height
        dw = w - self.proxy.state['width']
        dh = h - self.proxy.state['height']

        if (dw,dh) == (0,0):
            return        

        #ensure proxy state is updated
        self.proxy.state['height'] = h
        self.proxy.state['width']  = w
        
        self.proxy.resized(dw, dh)
        
    def setContainer(self,container):
        if not application().isRunning(): return
        if container is None: return
        if self.widget is None:
            self.create()
        self.proxy.push(blocked=['container'])
        # Ensure contents are properly created.
        for comp in self.proxy.contents:
            comp.container = self.proxy

    def setGeometry(self, x, y, width, height):
        if not self.widget: return
        self.widget.set_uposition(x, y)
        self.widget.set_default_size(width, height)

class MenuWrapper:
    pass

class MenuCommandWrapper:
    pass

class MenuCheckWrapper:
    pass

class MenuSeparatorWrapper:
    pass

class MenuBarWrapper:
    pass


class Application(AbstractApplication):
    """
    Wraps a backend Application object (or implements one from
    scratch if necessary).

    wxgui's Application class inherits wxPython's Application class.
    On the other hand, Tk has no Application class, so tkgui's
    Application class simply calls Tk.mainloop() in its
    Application.internalRun() method.
    """
    def __init__(self, **kwds):
        AbstractApplication.__init__(self, **kwds)
        self._isRunning = True
        
    def isRunning(self): return self._isRunning
    def internalRemove(self):        
        if not self._windows:
            gtk.main_quit()
            
    def internalRun(self):
        """
        Do whatever is necessary to start your backend's event-
        handling loop.
        """
        gtk.main()

