from .subsystem import Subsystem

class Fan(Subsystem):
    _name = "fan"

    _states = [
        "STOPPED",
        "RUNNING",
        "FAULT",
        "ESTOP"
    ]

    def __init__(self, client):
        Subsystem.__init__(self, client)
        Subsystem.__init_complete__(self)

    def state(self):
        s = Subsystem.state(self)

        return s
