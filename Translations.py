import gettext

class Translations:

    language = "en_gb"

    def __init__(self, iso=""):
        if locale:
            self.change_locale(iso)
    
        gettext.bindtextdomain("muon", "Languages")
        gettext.textdomain("muon")

        self.translator = gettext.gettext 

    def change_locale(self, iso):
        """ Changes to another locale based on an ISO code 
        """
        self.language = iso
        
