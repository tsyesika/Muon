# -*- coding: utf-8 -*-
import time
import re

class Controller:

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
    _screen = [] # what's on the screen and where
    _keymap = {}
    
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

        elif "i" == key:
            # ignore.
            pass
       
        self.update()
     
    def get_focus(self):
        """ returns the ID of which item is in focus (or None if no item is in focus) """
        if "" == self.__focus:
            return None
        return self.__focus

    def post_note(self, note):
        """ Takes note object """
        oid = note["object"]["id"].split(":", 1)[1] # object id
        for item in self._screen:
            if item["id"] == oid:
                return False# don't want duplicates
        content = self.convertHTML(note["content"])
        content = self.fixJPopeBug(content)
        ts = time.time() # please fix me
        #ts = self.convertTime(note["object"]["published"])
        try:
            actor = note["actor"]["preferredUsername"]
        except:
            actor = "[Unknown]"
        
        # okay now make the dict and add it to the screen
        item = {
            "id":oid,
            "actor":actor,
            "content":content,
            "time":ts,
            "focus":False
        }

        self._screen.append(item) 
        # for now we'll fix it at 25 items
        self._screen = self._screen[:25]
        return True # to say we added it

    def update(self):
        """ Updates the screen """
        self.master.update(self._screen)

    def convertTime(self, ts):
        """ Converts a time to a unix timestamp """
        ts = time.strptime("%Y-%m-%dT%H:%M:%SZ", ts)
        return ts
    
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
