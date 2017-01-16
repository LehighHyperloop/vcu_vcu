from .subsystem import Subsystem

class Wheels(Subsystem):
    _name = "wheels"

    _states = [
        "UP",
        "DOWN",
        "FAULT",
        "ESTOP"
    ]

    def __init__(self, client):
        Subsystem.__init__(self, client)
        Subsystem.__init_complete__(self)

    def state(self):
        s = Subsystem.state(self)

        return s
