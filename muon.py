#!/usr/bin/python3

# Python stdlib
import gettext

# 3rd Party
from PyPump.PyPump import PyPump

# Muon
from configuration import configuration
from interface import interface

class Muon:
    def __init__(self):
        
        self.interface = interface
        
        # so do we have any accounts?
        if not configuration or True:
            # okay lets tell the interface to display the 
            # new account view
            self.interface.change_view("new_account")
            self.interface.get_view().run()
        else:
            self.interface.change_view("message")
            self.interface.get_view().run()

if __name__ == "__main__":
    muon = Muon()
