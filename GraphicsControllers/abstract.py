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

class Controller:

    _screen = [] # what's on the screen and where
    _keymap = {}
    
    def __init__(self, master):
        """ Initalises graphics controller and takes the master GC """
        self.master = master
        self.HTMLStripper = re.compile(r'<[^<]+?>')

    def createID(self, note):
        """ The ID given is for the item not the act so we need to make one """
        hashable = str(note)
        hashable = hashable.encode()
        return sha1(hashable).hexdigest()

    def exit(self):
        self._screen = {}
        self.update()

    def fixJPopeBug(self, content):
        """ Converts JPope's UTF-something to 'JPope' until a better solutions found """
        for i, item in enumerate(content):
            content[i] = item.replace("ⒿⓅⓄⓅⒺ", "JPope")
        
        return content
 
    def handle_input(self, key):
        """ Handles the input for the view """
        pass

    def id_to_index(self, item_id):
        """ This convers the id to the index in the Pile """
        # returns None if no item is in focus
        if "" == item_id:
            return None

        for index, item in enumerate(self._screen):
            if item["id"] == item_id:
                return index

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
    
    def update(self):
        """ Updates the screen """
        self.master.update(self._screen)

    def convertHumanTime(self, ts):
        """ Takes a unix time stamp and converts it to human time """
        t = time.time()-ts # difference from current time and posted time
        
        if t < 60:
            return "Less than a minute"
        elif (t / 60) <= 60:
            # a hour
            m = int(t/60.0 + .5) # .5 to avoid floor rounding.
            if m <= 1:
                return "A minute"
            else:
                return "%s minutes" % m
        elif ((t / 60) / 60) <= 24:
            # a day
            h = int(t / 60.0 / 60.0 + 0.5)
            if h <= 1:
                return "An hour"
            else:
                return "%s hours" % h
        elif (((t / 60) / 60) / 24) <= 7:
            # a week
            d = int(t / 60.0 / 60.0 / 24.0 + 0.5)
            if d <= 1:
                return "A day"
            else:
                return "%s days" % d
        elif ((((t / 60) / 60) / 24) / 7) <= 4:
            # a month (29 days, lowest except 28)
            w = int(t / 60.0 / 60.0 / 24.0 / 7.0 + 0.5)
            if w <= 1:
                return "A week"
            else:
                return "%s weeks" % w
        elif (((t / 60) / 60) / 24) <= 365 :
            # a year
            m = int(t / 60.0 / 60.0 / 24.0 / 7.0 / 4.0 + 0.5)
            if m <= 1:
                return "A month"
            else:
                return "%s months" % m
        elif ((((t / 60) / 60) / 24) / 365) <= 10:
            # a decade (decade - century)
            y = int(t / 60.0 / 60.0 / 24.0 / 365.0 + 0.5)
            if y <= 1:
                return "A year"
            else:
                return "%s years" % y
        elif ((((t / 60) / 60) / 24) / 365) <= 100:
            # a century
            d = int(t / 60.0 / 60.0 / 24.0 / 365.0 / 10 + 0.5)
            if d <= 1:
                return "A decade"
            else:
                return "%s decades" % y
        else:
            c = int(t / 60.0 / 60.0 / 24.0 / 365.0 / 100.0 + 0.5)
            if c <= 1:
                return "A century"
            else:
                return "%s centuries" % c

    def convertHTML(self, content):
        """ Convers the content of a message from HTML to an outputtable form """
        # for now lets just handle <br />
        content = content.split("<br />")
        
        # strip the rest of the html out.
        displayable = []
        for item in content:
            displayable.append(
                self.HTMLStripper.sub("", item)
            )
        
        return displayable

    def convertTime(self, ts):
        """ Converts a time to a unix timestamp """
        ts = time.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
        return time.mktime(ts)
