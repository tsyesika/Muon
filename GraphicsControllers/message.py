# -*- coding: utf-8 -*-

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

import time
import re

from hashlib import sha1

from GraphicsControllers.abstract import Controller as Abstract

class Controller(Abstract):

    """
    Screen will contain (example):
    [
        {
            "id":"SomeObjectID"
            "actor":"Tsyesika",
            "content":"Message",
            "time":1363985334.709884,
            "focus":False # must only be set on one.
        }
    ]
    This must be a list to preserve order
    """
    
    ##
    # This is for which item is in focus
    # This is for internal use ONLY
    # -
    # The reason for this being the ID and not just an int
    # is for when notes are added later, if we save it to the config
    # later on and most importantly, when you hit enter it should take
    # you to a page for that item, so much easier with an ID.
    ##
    __focus = ""

    def handle_input(self, key):
        """ Handles the input for the view """
        # Selecting needs to work.
        if "down" == key:
            if "" == self.__focus:
                self.__focus = self._screen[0]["id"]
                self._screen[0]["focus"] = True
                self.update()
                return

            index = self.id_to_index(self.__focus) 
            try:
                self._screen[index]["focus"] = False
                index += 1
                self.__focus = self._screen[index]["id"]
                self._screen[index]["focus"] = True
            except:
                self.__focus = self._screen[0]["id"]
                self._screen[0]["focus"] = True

        if "up" == key:
            if "" == self.__focus:
                self.__focus = self._screen[0]["id"]
                self._screen[0]["focus"] = True
                self.update()
                return
            index = self.id_to_index(self.__focus)
            if index <= 0:
                self._screen[index]["focus"] = False
                index = len(self._screen)-1
                self.__focus = self._screen[index]["id"]
                self._screen[index]["focus"] = True
            else:
                self._screen[index]["focus"] = False
                index -= 1
                self.__focus = self._screen[index]["id"]
                self._screen[index]["focus"] = True

        elif "enter" == key and self.__focus:
            # okay we want to switch views to item view.
            pumpid = self.get_focused_pumpid()
            self.master.change_view("item")
            self.master.backend.get_item(pumpid)
            return 

        elif "i" == key:
            # ignore.
            pass
       
        self.update()

    def get_focus(self):
        """ returns the ID of which item is in focus (or None if no item is in focus) """
        if "" == self.__focus:
            return None
        return self.__focus
 
    def set_focus(self, oid):
        """ Sets the focus based on an object id """
        self.__focus = oid

    def get_focused_pumpid(self):
        """ Gets the pump id for a focused item or returns None if nothing is in focus """
        if not self.__focus:
            return None

        for note in self._screen:
            if note["id"] == self.__focus:
                return note["pumpid"]
 
    def populate(self):
        """ Populates view with what's needed """
        self.master.backend.meanwhile()
   
    def post_note(self, note):
        """ Takes note object """
        oid = self.createID(note) # object id
        for item in self._screen:
            if item["id"] == oid:
                return False # don't want duplicates

        content = self.convertHTML(note["content"])
        content = self.fixJPopeBug(content)
        ts = self.convertTime(note["object"]["published"])
        ts = self.convertHumanTime(ts)
        
        try:
            actor = note["actor"]["preferredUsername"]
        except:
            actor = "Unknown"
        
        # decide on the focus
        focus = False
        if self.__focus == note["object"]["id"]:
            focus = True
 
        pumpid = note["object"]["id"]
        if pumpid.startswith("http"):
            pumpid = pumpid.split("/")[-1]

        # okay now make the dict and add it to the screen
        item = {
            "id":oid,
            "pumpid":pumpid,
            "actor":actor,
            "content":content,
            "time":ts,
            "focus":focus
        }

      
        
        self._screen.insert(0, item) 
        # for now we'll fix it at 25 items
        self.update()
        return True # to say we added it
