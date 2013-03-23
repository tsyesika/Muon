import urwid
import sys

class View():
  
    def __init__(self, display):
        """ initalised the curses interface """
        self.display = display
        self.notes = urwid.Pile([], 0) # all the notes
        self.collection = urwid.Filler(
                urwid.Padding(self.notes, align='left', left=10, right=10),
                'top',
                top=5,
                bottom=10
        )        
        
        self.display.add_widget(self.collection)

    def refocus(self, focus):
        """ Applies focuses """
        for number, item, in enumerate(self.notes.contents):
            if number == focus:
                # apply the focus
                self.notes.contents[number][0].set_attr_map({None:'focus'})
            else:
                self.notes.contents[number][0].set_attr_map({None:'normal'})
 
    def update(self, screen):
        # remove the old stuff
        for item in self.notes.contents:
            self.notes.contents.remove(item)
        # add new
        for item in screen:
            self.notes.contents.append(
                (urwid.AttrMap(
                    urwid.Text(
                        item["content"]
                        ), "normal"
                    ),
                 self.notes.options())
            )
 
        # finally we'll force draw the screen
        self.display.redraw()
    def input_handler(self, key):
        """ Handles input """
        if "c" == key:
            self.display.clear()
            self.__init__(self.display)
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
    
    def __del__(self):
        pass 
