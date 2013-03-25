##                                                                      
# This file is part of Muon.                                            
#                                                                       
# Muon is free software: you can redistribute it and/or modify          
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, either version 3 of the License, or     
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
