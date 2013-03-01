import imp
import glob
import os

class Interface():
    current_view = None
    views = {}

    def __init__(self):
        # load views
        for view in glob.glob("Views/*.py"):
            name = os.path.splitext(os.path.basename(view))[0]
            self.views[name] = imp.load_source(name, view)
    
    def get_view(self):
        if None == self.current_view:
            raise Exception("No view selected")
        else:
            return self.current_view.view 

    def change_view(self, view):
        try:
            self.current_view = self.views[view]
        except:
            raise
            
interface = Interface()    
