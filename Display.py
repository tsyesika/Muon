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

class Display():
    _pallet = [
        ('background', 'white', 'black'),
        ('focus', 'black', 'light gray'),
        ('normal', 'default', 'black')
    ]

    _elements = []
    _background = None # fixed.
    _display = None

    def __init__(self, gc):
        """ Initalises the display """
        self._gc = gc
        self._background = urwid.SolidFill()
        self._display = urwid.MainLoop(
                                self._background,
                                self._pallet,
                                unhandled_input=self.input_handler
        )  

        self._display.widget = urwid.AttrMap(
                                    self._background,
                                    'background'
        )

        self._display.widget.original_widget = urwid.Pile([], 0)

    def run(self):
        """ Displays the Display (yes, seriously) """
        self._display.run()

    def redraw(self):
        """ Use with care """
        self._display.draw_screen()

    def clear(self):
        """ Clears the elements off the display """
        # go through rmeoving the reference
        for element in self._elements:
             self._elements.remove(element)

        # double check people haven't been sneeky.
        self._display.widget.original_widget.contents = []

    def input_handler(self, key):
        """ Hands the input back to the graphics controller """
        self._gc.handle_input(key)

    def update(self, screen):
        self._gc.update(screen)

    def add_widget(self, widget):
        """ This will add a widget to the display """
        self._elements.append(widget)
        self._display.widget.original_widget.contents.append((
            widget,
            self._display.widget.original_widget.options()
        )) 

    def exit(self):
        """ Passes the exit to GraphicsController """
        self._gc.exit()
