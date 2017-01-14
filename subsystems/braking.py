from .subsystem import Subsystem

class Braking(Subsystem):
    _name = "Braking"

    _states = [
        "OFF",
        "ON",
        "FAULT",
        "ESTOP"
    ]

    def __init__(self, client):
        Subsystem.__init__(self, client)
        Subsystem.__init_complete__(self)

    def state(self):
        s = Subsystem.state(self)

        return s
