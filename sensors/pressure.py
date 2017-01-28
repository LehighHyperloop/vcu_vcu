from .sensor import Sensor

import collections
import time

class Pressure(Sensor):
    _name = "pressure"
    _location = "all"

    _levitation = 0
    _pneumatics = 0

    def handle_status_update(self,msg_json):
        self._last_update = time.time()

        self._levitation = float(msg_json["levitation"])
        self._pneumatics = float(msg_json["pneumatics"])

    def __repr__(self):
        return self._location + "/" + \
            self._name + "(" + \
            "levitation: " + str(self._levitation) + ", " + \
            "pneumatics: " + str(self._pneumatics) + \
            ") " + str(self.last_update()) + "s"
