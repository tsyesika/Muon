##                                                                      
# This file is part of Muon.                                            
#                                                                       
# Muon is free software: you can redistribute it and/or modify          
# it under the terms of the GNU General Public License as published by  # the Free Software Foundation, either version 3 of the License, or     
# (at your option) any later version.                                   
#                                                                       
# Muon is distributed in the hope that it will be useful,               
# but WITHOUT ANY WARRANTY; without even the implied warranty of        
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          
# GNU General Public License for more details.                          
#                                                                       
# You should have received a copy of the GNU General Public License     
# along with Muon. If not, see <http://www.gnu.org/licenses/>.          
## 

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
    _controller = None

    _views = {}
    _controllers = {}    

    _keymap = {
    } # global non-overridable keys

    
    _previous_view_name = "" # view name
    _previous_focus = "" # focus id on previous screen

    def __init__(self, backend):
        # load the views
        self.load_views()
        self.load_controllers()

        self.backend = backend
        self.display = Display(self)
    
        self._keymap["esc"] = ["self._controller.exit", "self.backend.exit"]

    def run(self):
        self.display.run()

    def change_view(self, view, params=()):
        """ Will change the view """
        # does the view we want exist?
        if not view in self._views:
            raise ControllerException("Can't find view named %s" % view)        

    
        if self._view != None:
            # sets previouses.
            self._previous_view_name = self._view.get_name()
            self._previous_focus = self.controller().get_focus()
            if self._previous_focus == None:
                self._previous_focus = ""

        # view exists.
        if None != self._view:
            self._view.__del__()
            self.display.clear()
        if params:
            self._view = self._views[view].View(self.display, params)
        else:
            self._view = self._views[view].View(self.display)

        self._controller = self._controllers[view].Controller(self)

    def back_view(self):
        """ Returns to the last view """
        if not self._previous_view_name:
            return # can't do it
        focus = self._previous_focus
        self.change_view(self._previous_view_name)
        self.controller().set_focus(focus)
        self.controller().populate()
    
    def handle_input(self, key):
        """ This is the glue between handling purely view 
            input (e.g. adding a letter on the screen)
            and speaking to the backend when an input is made
            that requires change on the backend
        """
        # for now just pass it across it to display
        if type(key) in [tuple]:
            return # we don't support mouse

        if self._view:
            if key in self._keymap:
                # global override.
                for call in self._keymap[key]:
                    getattr(self, call)()
            else:
                # okay now hand it off to the specific GC
                self._controller.handle_input(key)

    def controller(self):
        """ Returns the current view GC, if none, returns self """
        if self._controller:
            return self._controller
        return self

    def update(self, screen):
        """ This will update the screen """
        # ensure the screens clear
        self._view.clear()
        self._view.update(screen)

    def load_views(self):
        """ This will load the views """
        for view in glob("Views/*.py"):
            name = self.path_to_name(view)
            self._views[name] = load_source(name, view)

    def load_controllers(self):
        """ Loads the GC's """
        for controller in glob("GraphicsControllers/*.py"):
            name = self.path_to_name(controller)
            self._controllers[name] = load_source(name, controller)

    def path_to_name(self, path):
        """ This will take a path convert to a name """
        base_name = os.path.basename(path)
        name = os.path.splitext(base_name)[0]
        return name
