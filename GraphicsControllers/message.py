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
            "time":1363985334.709884
        }
    ]
    This must be a list to preserve order
    """
    _screen = [] # what's on the screen and where
    _keymap = {}

    def __init__(self, master):
        """ Initalises graphics controller and takes the master GC """
        self.master = master
        self.HTMLStripper = re.compile(r'<[^<]+?>')

    def handle_input(self, key):
        """ Handles the input for the view """
        pass

    def remove_filter(self, f):
        """ Filters the notes on the screen - mainly used for removing ignored items 
            if the attribute isn't set it will ignore it when filtering
            NB: if it matches the fillter it WILL be removed.
        """
        for item in self._screen:
            for key in f.keys():
                if key in item and self._screen[key] == f[key]:
                    self._screen.remove(item)

    def post_note(self, note):
        """ Takes note object """
        oid = note["object"]["id"].split(":", 1)[1] # object id
        for item in self._screen:
            if item["id"] == oid:
                return # don't want duplicates
        content = self.convertHTML(note["content"])
        content = self.fixJPopeBug(content)
        ts = time.time()
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
        }

        self._screen.insert(0, item) # adds it to the top 
        
        # for now we'll fix it at 25 items
        self._screen = self._screen[:25]

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
