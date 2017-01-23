import collections

class Accel():
    _client = None

    _prefix = "sensor/"
    _name = "accel"
    _location = None

    _buffer = collections.deque(maxlen=10)

    def __init__(self, client, location):
        self._client = client
        self._location = location

    def get_topic(self):
        return self._prefix + self._location + "/" + self._name

    def handle_status_update(self,msg_json):
        self._buffer.append( (msg_json["x"], msg_json["y"], msg_json["z"]) )

    def rolling_avg(self):
        total = [0,0,0]
        for v in self._buffer:
            for i in xrange(0,2):
                total[0] += float(v[i])

        return (total[0] / len(self._buffer),
                total[1] / len(self._buffer),
                total[2] / len(self._buffer))

    def __repr__(self):
        if len(self._buffer) > 0:
            v = self._buffer[-1]
            return self._name + "(" + \
                "x: " + v[0] + \
                ", y: " + v[1] + \
                ", z: " + v[2] + \
                ")" + str(self.rolling_avg())

        return self._name + "()"
