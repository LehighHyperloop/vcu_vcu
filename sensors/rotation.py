from .sensor import Sensor

import collections
import copy
import time

class Rotation(Sensor):
    _name = "rotation"
    _location = "right"

    _speed = 0
    _last_t = 0
    _ticks = 0

    circumference_in_m = 2 * 3.14 * (15.5/2) * 2.54 / 100

    def handle_status_update(self,msg_json):
        self._last_update = time.time()
        self._speed = float(msg_json["rps"]) * self.circumference_in_m
        self._last_t = int(msg_json["last_t"])
        self._ticks = int(msg_json["ticks"])

    def velocity(self):
        return self._speed

    def distance(self):
        return self._ticks * self.circumference_in_m / 2

    def __repr__(self):
        return self._location + "/" + \
            self._name + "(" + \
            "speed: " + str(self._speed) + ", " + \
            "last_t: " + str(self._last_t) + ", " + \
            "ticks: " + str(self._ticks) + ", " + \
            "distance: " + str(self.distance()) + \
            ") " + str(self.last_update()) + "s"
