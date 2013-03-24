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

import urwid
import sys

from Views.abstract import View as Abstract_View

class View(Abstract_View):
  
    __name = "message"

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
                (urwid.Columns([
                    urwid.AttrMap(urwid.Text(
                        item["content"],
                        align="left"
                        ), style),
                    urwid.AttrMap(urwid.Text(
                        item["time"],
                        align="right"
                        ), style
                    ), 
                ]), self.notes.options())
            )
           
 
        # finally we'll force draw the screen
        self.display.redraw()
