from .sensor import Sensor

import collections
import time

class SuspensionDistance(Sensor):
    _name = "distance"
    _location = "suspension"
    _buffer = collections.deque(maxlen=10)

    def handle_status_update(self,msg_json):
        self._last_update = time.time()
        self._buffer.append( (float(msg_json["fl"]), float(msg_json["fr"]), float(msg_json["rl"]), float(msg_json["rr"])) )

    def __repr__(self):
        if len(self._buffer) > 0:
            v = self._buffer[-1]
            return self._location + "/" + \
                self._name + "(" + \
                "raw: ({:0.3f}, {:0.3f}, {:0.3f}, {:0.3f}) ".format(v[0],v[1],v[2],v[3]) + \
                ") " + str(self.last_update()) + "s"

        return self._location + "/" + \
            self._name + "() " + str(self.last_update()) + "s"
