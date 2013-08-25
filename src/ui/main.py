import time
import sys
import urwid

class Messages(urwid.SimpleListWalker):
    """
        Container for the main body of information in a list
        Possible to add to a position or end of list by using

        Messages.add(item, position=None)

    """

    def __init__(self, *args, **kwargs):
        contents = kwargs.get("contents", list())
        kwargs["contents"] = contents
        super(Messages, self).__init__(*args, **kwargs)
        self.focus = 0

    def add(self, item, position=None):
        if position is None:
            self.append(item)
        elif len(sef) < position:
            self[position] = item
        else:
            # index doesn't exist yet so just append
            self.append(item)

        if len(self) == 1:
            self.set_focus(0)

    def set_focus(self, position):
        """ Applies the focus """
        for i, item in enumerate(self):
            text = item.base_widget
            if i == position:
                self[i] = urwid.AttrMap(text, "focus")
            else:
                self[i] = urwid.AttrMap(text, "normal")
        

class CLI(object):

    _pallet = [
        ("background", "white", "black"),
        
        ("top_bar", "black", "white"),
        ("bottom_bar", "black", "white"),
        
        ("focus", "light magenta", "black"),
        ("normal", "default", "black"),
    ]

    _hive = None
    _run = False
    _display = None
    _background = None
    _list = None
    _frame = None

    def __init__(self, hive, *args, **kwargs):
        super(CLI, self).__init__(*args, **kwargs)
        self._hive = hive
        self._background = urwid.SolidFill()
        urwid.set_encoding("utf-8") 
        self._display = urwid.MainLoop(
                self._background,
                self._pallet,
                unhandled_input=self.input_handler
                )

        self._display.widget = urwid.AttrMap(
                self._background,
                "background"
                )

        self._stack = Messages()
        self._list = urwid.ListBox(self._stack)
        self._frame = urwid.Frame(urwid.AttrMap(self._list, "normal"))
        self._display.widget.original_widget = self._frame

    def start_gui(self):
        self._run = True
    
    def stop_gui(self):
        self._run = False

    def run(self):
        """ Runs the screen """
        while self._display is not None:
            if self._run:
                self._display.run()
            time.sleep(1)

    def quit(self):
        """ Exits the screen """
        self._display = None
        self._hive.send_shutdown()
        raise urwid.ExitMainLoop
    
    def clear(self):
        """ Clear's the display """
        for elem in self._stack.contents:
            self._stack.contents.remove(elem)

    def redraw(self):
        """ Redraws the screen - use with care """
        if self._display is not None:
            self._display.draw_screen()

    def draw_bars(self, top=None, bottom=None, redraw=True):
        """ Draws the two bars a the top and bottom of the screen """
        if top is not None:
            top = urwid.Text(top)
            top_bar = urwid.AttrMap(top, "top_bar")
            self._frame.header = top_bar
        
        if bottom is not None:
            bottom = urwid.Text(bottom)
            bottom_bar = urwid.AttrMap(bottom, "bottom_bar")
            self._frame.footer = bottom_bar

        if redraw:
            self.redraw()

    def add_from_inbox(self, activity):
        """ Adds an activity from pump """
        index = len(self._stack)+1
        status = "N"
        date = activity.updated.strftime("%b %d %H:%M")
        poster = activity.actor.display_name[:25]
        contents = getattr(
            activity.obj,
            "content",
            getattr(activity.obj, "display_name", str(activity))
            )
        if contents is None:
            return

        contents = contents[:50].replace("\n", "")
        
        verb = activity.verb
        if verb.find("/") != -1:
            verb = verb.split("/")[-1]
        elif verb.endswith("e"):
            verb += "d"
        else:
            verb += "ed"
        
        body = u"{verb} {contents}".format(verb=verb, contents=contents)
        line = "%4s   %s  %10s  %25s    %s" % (index, status, date, poster, body)
        line = urwid.AttrMap(urwid.Text(line), "normal")
        self._stack.add(line)

    def draw_inbox(self):
        """ Draw's the main timeline """
        self.clear()

        # draw the top bar with key help
        self.draw_bars(
            top="Muon -- q:Quit  R:Refesh  m:New Note  r:Reply",
            bottom="Fetching Messages..."
            )

        # redraw the screen
        self.redraw() 

        # now ask pump to get the messages
        self.input_handler("R")
  
        self._hive.send_message(
            to="pump",
            directive="fetch_inbox",
            body=(
                self.add_from_inbox,
                self.redraw,
                lambda :self.draw_bars(bottom="Ready!"))
            )

    def input_handler(self, key):
        """ Handles the input """
        if key == "q":
            self.quit()
        elif key == "R":
            # Refresh
            self.draw_inbox
