from .subsystem import Subsystem

class Compressor(Subsystem):
    _name = "compressor"

    _states = {
        "DISABLED":             0,
        "VFD_STARTING":         1,
        "COMPRESSOR_STARTING":  2,
        "RUNNING":              3,
    }

    _pressure = 0

    def __init__(self):
        Subsystem.__init__(self)
        Subsystem.__init_complete__(self)

    def handle_status_update(self, msg_json):
        Subsystem.handle_status_update(self, msg_json)

        # TODO: Handle pressure
        self._pressure = msg_json["pressure"]

    def state(self):
        s = Subsystem.state(self)
        s.update({
            "pressure": self._pressure
        })

        return s
