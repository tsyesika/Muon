import urwid
import sys

class Message():
    pallet = [
        ('bg', 'white', 'black'),
        ('focus', 'black', 'light gray'),
        ('normal', 'default', 'black')
    ]

    def __init__(self):
        """ initalised the curses interface """
        self.background = urwid.SolidFill()
        self.loop = urwid.MainLoop(self.background, self.pallet, unhandled_input=self.input_handler)
        
        # make the pile of notes
        self.notes = urwid.Pile([], 0)
        self.collection = urwid.Filler(
                urwid.Padding(self.notes, align='left', left=10, right=10),
                'top',
                top=5,
                bottom=10
        )        
        
        # attach the background & pile
        self.loop.widget = urwid.AttrMap(self.background, 'bg')
        self.loop.widget.original_widget = self.collection

    def run(self):
        self.loop.run() 

    def refocus(self, focus):
        """ Applies focuses """
        for number, item, in enumerate(self.notes.contents):
            if number == focus:
                # apply the focus
                self.notes.contents[number][0].set_attr_map({None:'focus'})
            else:
                self.notes.contents[number][0].set_attr_map({None:'normal'})
 
    def input_handler(self, key):
        """ Handles input """
        if "q" == key:
            # quitting
            raise urwid.ExitMainLoop
        elif "e" == key:
            # add an example
            self.notes.contents.insert(0, (urwid.AttrMap(urwid.Text('[Tsyesika] Blah '), 'normal'), self.notes.options()))     
        elif "up" == key:
            try:
                self.notes.contents.focus -= 1
            except:
                self.notes.contents.focus = len(self.notes.contents)-1
            self.refocus(self.notes.contents.focus)
            
        elif "down" == key:
            try:
                self.notes.contents.focus += 1
            except:
                self.notes.contents.focus = 0
            self.refocus(self.notes.contents.focus)
        
view = Message()
