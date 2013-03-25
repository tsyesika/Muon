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
        
