import time
from xudd.actor import Actor
from pypump import PyPump

class Pump(Actor):
    
    pump = None
    me = None

    def __init__(self, *args, **kwargs):
        super(Pump, self).__init__(*args, **kwargs)
        self.message_routing.update({
            "fetch_inbox": self.fetch_inbox,
            "setup": self.setup,
        })

    def setup(self, message):
        """ Sets up pypump object """
        try:
            webfinger = message.body["webfinger"]
            self.pump = PyPump(
                webfinger,
                client_name="Muon",
                client_type="native",
                key=message.body["key"],
                secret=message.body["secret"],
                token=message.body["token"],
                token_secret=message.body["token_secret"]
                )
            webfinger = message.body["webfinger"]
        
        except KeyError:
            webfinger = raw_input("Webfinger: ").lstrip(" ").rstrip(" ")
            self.pump = PyPump(
                webfinger,
                client_name="Muon",
                client_type="native"
                )

            config = {
                "webfinger": webfinger,
                "key": self.pump.get_registration()[0],
                "secret": self.pump.get_registration()[1],
                "token": self.pump.get_token()[0],
                "token_secret": self.pump.get_token()[1],
            }

            self.hive.send_message(
                to="muon",
                directive="write_config",
                body=config
                )

        self.me = self.pump.Person(webfinger)

        self.send_message(
            to="muon",
            directive="start_gui"
            )

    def fetch_inbox(self, message):
        if self.me is None:
            time.sleep(1)
            return self.fetch_inbox(message)

        appender, redraw, update = message.body
        inbox = self.me.inbox[:100]
        for activity in inbox:
            appender(activity)
            redraw()

        update()

