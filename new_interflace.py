import urwid
import random
import sys
def handle_input(key):
    people = ["zmoylan", "evan", "moggers87", "Tsyesika"]
    if key == "e":
        pile_of_notes.widget_list.insert(0, urwid.Text('[%s] Blah blah, huge bitch' % random.choice(people)))
    elif key == "q":
        raise urwid.ExitMainLoop

class Interface():
    pallet = [
        ('bg', 'white', 'black'),
        ('focus', 'white', 'dark green'),
        ('normal', 'white', 'black')
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
        self.notes.keypress(key)
        if "q" == key:
            # quitting
            raise urwid.ExitMainLoop
        elif "e" == key:
            # add an example
            self.notes.contents.insert(0, (urwid.AttrMap(urwid.Text('[Tsyesika] Example'), 'focus'), self.notes.options()))     
            self.refocus(0)
        elif "up" == key:
            self.refocus(self.notes.contents.focus)
        
        elif "down" == key:
            self.refocus(self.notes.contents.focus)
        
if __name__ == "__main__":
    interface = Interface()
    
