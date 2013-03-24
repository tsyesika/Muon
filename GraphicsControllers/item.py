# -*- coding: utf-8 -*-
import time
import re

from hashlib import sha1

class Controller:

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
    _screen = [] # what's on the screen and where
    _keymap = {}
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

    def __init__(self, master):
        """ Initalises graphics controller and takes the master GC """
        self.master = master
        self.HTMLStripper = re.compile(r'<[^<]+?>')

    def idToIndex(self, item_id):
        """ This convers the id to the index in the Pile """
        # returns None if no item is in focus
        if "" == item_id:
            return None

        for index, item in enumerate(self._screen):
            if item["id"] == item_id:
                return index

    def log(self, msg):
        f = open("log.txt", "a")
        f.write("%s\n" % msg)
        f.close()

    def handle_input(self, key):
        """ Handles the input for the view """
        # Selecting needs to work.
        if "down" == key:
            if "" == self.__focus:
                self.__focus = self._screen[0]["id"]
                self._screen[0]["focus"] = True
                self.update()
                return

            index = self.idToIndex(self.__focus) 
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
            index = self.idToIndex(self.__focus)
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
    
    def createID(self, note):
        """ The ID given is for the item not the act so we need to make one """
        hashable = str(note)
        hashable = hashable.encode()
        return sha1(hashable).hexdigest()

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

    def update(self):
        """ Updates the screen """
        self.master.update(self._screen)

    def convertTime(self, ts):
        """ Converts a time to a unix timestamp """
        ts = time.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
        return time.mktime(ts)

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
    def fixJPopeBug(self, content):
        """ Converts JPope's UTF-something to 'JPope' until a better solutions found """
        for i, item in enumerate(content):
            content[i] = item.replace("ⒿⓅⓄⓅⒺ", "JPope")
        
        return content
    
    def exit(self):
        self._screen = {}
        self.update()
