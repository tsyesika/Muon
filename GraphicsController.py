from Display import Display
from imp import load_source  
from glob import glob

import os
import threading

from urwid import ExitMainLoop

class ControllerException(Exception):
    pass


class Controller:

    _view = None
    _views = {}

    def __init__(self, backend):
        # load the views
        self.load_views()

        self.backend = backend
        self.display = Display(self)
    
    def run(self):
        self.display.run()
    
    def change_view(self, view):
        """ Will change the view """
        # does the view we want exist?
        if not view in self._views:
            raise ControllerException("Can't find view named %s" % view)
        
        # okay now we know it exists we need to clear and switch.
        if None != self._view:
            self._view.__del__()
            self.display.clear()
        self._view = self._views[view].View(self.display)

    def handle_input(self, key):
        """ This is the glue between handling purely view 
            input (e.g. adding a letter on the screen)
            and speaking to the backend when an input is made
            that requires change on the backend
        """
        # for now just pass it across it to display
        if self._view:
            self._view.input_handler(key)

    def load_views(self):
        """ This will load the views """
        for view in glob("Views/*.py"):
            name = self.path_to_name(view)
            self._views[name] = load_source(name, view)

    def path_to_name(self, path):
        """ This will take a path convert to a name """
        base_name = os.path.basename(path)
        name = os.path.splitext(base_name)[0]
        return name

    def exit(self):
        """ Extis """
        if self._view:
            # give them a chance to clear up.
            self.display.clear()
        raise ExitMainLoop
