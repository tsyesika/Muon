import urwid

class Display():
    _pallet = [
        ('background', 'white', 'black'),
        ('focus', 'black', 'light gray'),
        ('normal', 'default', 'black')
    ]

    _elements = []
    _background = None # fixed.
    _display = None

    def __init__(self, gc):
        """ Initalises the display """
        self._gc = gc
        self._background = urwid.SolidFill()
        self._display = urwid.MainLoop(
                                self._background,
                                self._pallet,
                                unhandled_input=self.input_handler
        )  

        self._display.widget = urwid.AttrMap(
                                    self._background,
                                    'background'
        )

        self._display.widget.original_widget = urwid.Pile([], 0)

    def run(self):
        """ Displays the Display (yes, seriously) """
        self._display.run()

    def clear(self):
        """ Clears the elements off the display """
        # go through rmeoving the reference
        for element in self._elements:
             self._elements.remove(element)

        # double check people haven't been sneeky.
        self._display.widget.original_widget.contents = []

    def input_handler(self, key):
        """ Hands the input back to the graphics controller """
        self._gc.handle_input(key)

    def add_widget(self, widget):
        """ This will add a widget to the display """
        self._elements.append(widget)
        self._display.widget.original_widget.contents.append((
            widget,
            self._display.widget.original_widget.options()
        )) 

    def exit(self):
        """ Passes the exit to GraphicsController """
        self._gc.exit()
