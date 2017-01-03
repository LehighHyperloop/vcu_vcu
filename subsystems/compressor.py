from .subsystem import Subsystem

class Compressor(Subsystem):
    _name = "compressor"

    _states = [
        "STOPPED",
        "VFD_STARTING",
        "COMPRESSOR_STARTING",
        "RUNNING",
        "COMPRESSOR_STOPPING",
        "VFD_STOPPING",
        "FAULT",
        "ESTOP"
    ]

    _pressure = 0

    def __init__(self, client):
        Subsystem.__init__(self, client)
        Subsystem.__init_complete__(self)

    def handle_status_update(self, msg_json):
        Subsystem.handle_status_update(self, msg_json)
        self._pressure = msg_json["pressure"]

    def state(self):
        s = Subsystem.state(self)
        s.update({
            "pressure": self._pressure
        })

        return s
