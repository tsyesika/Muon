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
            "note":"This is a note",
            "comments":[
                {
                    "content":"This is the first comment",
                    "time":123456789.0
                },
                {
                    "content":"This is the second comment",
                    "time":987654321.0
                }
        }
    ]
    This must be a list to preserve order
    """
    _active_id = "" # id of active item

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
        
        elif "left":
            # change back to message view
            self.master.back_view()
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
    
    def new_comment(self, comment):
        """ Adds a new comment to the screen """
        oid = self.createID(comment)
        content = comment.convertHTML(comment["content"])
    
        time = self.convertTime(comment["published"])
        time = self.convertHumanTime(time)
    
        try:
            actor = comment["author"]["preferredUsername"]
            actor = self.fixJPopeBug(actor)
        except:
            actor = "Unkown"

        actor = "[%s]" % actor

        self._screen["comments"].append(
            {
                "id":oid,
                "pumpid":comment["id"],
                "actor":actor,
                "content":content,
                "time":time
            }
        )
   
    def get_name(self):
        return "item"

    def new_item(self, item):
        """ Adds a new note to the screen """
        # pull out note stuff
        oid = self.createID(item)

        content = item["content"]
        content = self.convertHTML(content)
        
        time = self.convertTime(item["published"])
        time = self.convertHumanTime(time)
        
        try:
            actor = comment["author"]["preferredUsername"]
            actor = self.fixJPopeBug(actor)
        except:
            actor = "Unknown"
        
        actor = "[%s]" % actor
    
        self._screen.append(
            {
                "id":oid,
                "pumpid":item["id"],
                "actor":actor,
                "content":content,
                "time":time
            }
        )

        if item["replies"]["totalItems"] == 0:
            # not everyone love each other :(
            return

        for comment in item["replies"]["items"]:
            self.new_comment(comment)

    def get_active_id(self):
        return self._active_id

    def set_active_id(self, pumpid):
        """ Sets the current ID """
        self.__active_id = pumpid
