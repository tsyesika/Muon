import urwid
import sys

from Views.abstract import View as Abstract_View

class View(Abstract_View):

    __name = "item"
  
    def __init__(self, display):
        """ initalised the curses interface """
        self.display = display
        self.note = urwid.AttrMap(urwid.Text(""), "note")
        self.comments = urwid.Pile([], 0)

        self.contents = urwid.Pile([self.note, urwid.Divider("−") ,self.comments])

        self.collection = urwid.Filler(
                urwid.Padding(self.contents, align='left', left=10, right=10),
                'top',
                top=5,
                bottom=10
        )        
        
        self.display.add_widget(self.collection)

    def clear(self):
        """ Clears the screen """
        self.note.original_widget.set_text("")
        self.comments.contents = []

    def update(self, screen):
        """ Redraws the screen with screen """
        note = screen[0] # first thing, always is.
        self.note.original_widget.set_text(note["content"])
        
        comments = screen[1:] # everything after the note

        # add the comments
        for comment in comments:
            self.comments.contents.append(
                urwid.Columns([
                    urwid.AttrMap(urwid.Text(comment["content"]), "comment"),
                    urwid.AttrMap(urwid.Text(comment["time"], align="right"), "time")
                ])
            )

        # finally we'll force draw the screen
        self.display.redraw()
