import urwid
import sys

class View():
  
    def __init__(self, display):
        """ initalised the curses interface """
        self.display = display
        
        self.text = urwid.Pile([], 0)

        self.collection = urwid.Filler(
                urwid.Padding(self.text, align='left', left=10, right=10),
                'top',
                top=5,
                bottom=10
        )        
        
        self.display.add_widget(self.collection)

        self.verifier = "" # Verifier code
        self.wid = "" # webfingerID

        self.text.contents.append((
            urwid.Columns([]),
            self.text.options()
        ))

        self.text.contents[0][0].contents.append((
            urwid.Text("Enter your Webfinger: ", align='right'), self.text.contents[0][0].options()
        ))

        self.text.contents[0][0].contents.append((
            urwid.Text("username@example.com", align='left'), self.text.contents[0][0].options()
        ))

        self.text.contents.append((
            urwid.Divider(),
            self.text.options()
        ))

        self.text.contents.append((
            urwid.Text("If you're not already registered with a pump.io host, please register at http://pump.io/tryit",
                align='center'
            ),
            self.text.options()
        ))

    def __del__(self):
        pass

    def input_handler(self, key):
        """ Handles input """
        
        if "backspace" == key:
            self.wid = self.wid[:-1]

        else:
            # it must be desting for the text box :)
            self.wid += key
        
        self.text.contents[0][0].contents[1][0].set_text(self.wid)
