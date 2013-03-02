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
        self.box = urwid.Pile([])
        question = urwid.Edit(('bg', 'Webfinger ID: ',))
        self.box.contents.append((question, self.box.options()))
        
        self.box.contents.append((urwid.Divider(), self.box.options()))

        output = urwid.Text('Your webfinger ID is: ...')
        self.box.contents.append((output, self.box.options()))
        
        self.padding = urwid.Padding(self.box, left=20, right=20)

        self.loop.widget = urwid.AttrMap(self.background, 'bg')
        self.loop.widget.original_widget = urwid.Filler(self.padding, 'top')
        
        urwid.connect_signal(question, 'change', self.webfinger)
        self.webfinger_buff = ""

    def run(self):
        self.loop.run() 

    def webfinger(self, edit, webfinger):
        if webfinger == "enter":
            self.box.contents[1][0].set_text("Your webfinger ID is: %s" % self.webfinger_buff)
        else:
            self.webfinger_buff += webfinger

    def input_handler(self, key):
        """ Handles input """
        if "q" == key:
            # quitting
            raise urwid.ExitMainLoop
       
view = NewAccount()
