import os
import json
import time

from xudd.actor import Actor

class Controller(Actor):
    
    config = None

    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)
        self.message_routing.update({
            "setup": self.setup,
            "stop_gui": self.stop_gui,
            "start_gui": self.start_gui,
            "read_config": self.read_config,
            "write_config": self.write_config,
        })

        self.config = os.path.expanduser("~/.muon")

    def unpack(self, packet):
        for name, var in packet.items():
            setattr(self, name, var)

    def setup(self, message):
        self.unpack(message.body)
        self.hive.send_message(
            to="muon",
            directive="read_config"
            )

    def read_config(self, message):
        """ Reads config """
        try:
            config = json.loads(open(self.config).read())
        except (ValueError, IOError):
            # json's bad
            config = dict()

        self.hive.send_message(
            to="pump",
            directive="setup",
            body=config
            ) 

    def write_config(self, message):
        """ Writes config back to file """
        config = open(self.config, "w")
        jconfig = json.dumps(message.body)
        config.write(jconfig)
        config.close()

    def start_gui(self, message):
        self.gui.start_gui()
        time.sleep(1.25) # time it may take to get the GUI up
        self.gui.draw_inbox()

    def stop_gui(self, message):
        self.gui.quit()
