import urwid
import sys

class NewAccount(): 
    pallet = [
        ('bg', 'default', 'black')
    ]

    def __init__(self):
        """ initalised the curses interface """
        self.background = urwid.SolidFill()
        self.loop = urwid.MainLoop(self.background, self.pallet, unhandled_input=self.input_handler)

        # ask for the webfinger
        self.question = urwid.Edit(('bg', 'Webfinger ID: '))
        self.blah = urwid.Text('Your webfinger ID is: ...')
        self.loop.widget = urwid.AttrMap(self.background, 'bg')
        self.loop.widget.original_widget = self.question

        urwid.connect_signal(self.question, 'change', self.webfinger)

    def run(self):
        self.loop.run() 

    def webfinger(self, edit, webfinger):
        self.blah.set_text("Your webfinger ID is: %s" % webfinger)

    def input_handler(self, key):
        """ Handles input """
        if "q" == key:
            # quitting
            raise urwid.ExitMainLoop
       
view = NewAccount()
