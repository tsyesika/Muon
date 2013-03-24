import urwid
import sys

from Views.abstract import View as Abstract_View

class View(Abstract_View):
  
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

    def clear(self):
        """ Clears the screen """
        self.notes.contents = []

    def update(self, screen):
        # add new
        for item in screen:
            style = "normal"
            if item["focus"]:
               style = "focus"

            self.notes.contents.append(
                (urwid.AttrMap(
                    urwid.Text(
                        item["content"]
                        ), style
                    ),
                 self.notes.options())
            )
 
        # finally we'll force draw the screen
        self.display.redraw()
