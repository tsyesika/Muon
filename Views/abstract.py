import urwid

"""
Skeliton class of everything that needs to be there for any view.

Views should be kept very thin, the idea for them is that you pass
pre-prepared (by the view specific GC) items to then just be displayed
the view should NOT handle the input or be responsible for much. Keep it thin!!!
"""

class View:

    __name = "" # name of view.

    def __init__(self, display):
        self.display = display
        self.screen = urwid.Pile([], 0) # holds the items on the screen, highly suggest you use this.

    def get_name(self):
        """ Gets the name of the view """
        return self.__name

    def clear(self):
        """ This should clear what's on the screen """
        pass
            
    def update(self, screen):
        """ This will update the screen with screen a list of things to be displayed
        This will probably need to be re-written by _most_ if not all views the code below
        assumes screen (passed in) is a list of strings that need displaying.
        """
        self.clear()
        for item in screen:
            self.screen.contents.append(urwid.AttrMap(
                    urwid.Text(item), 
                    'normal'
                ), self.screen.options()
            )
        
    def __del__(self):
        """ This is called when the view is being switched away from """
        pass
