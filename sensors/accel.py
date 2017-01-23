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
        self._buffer.append( (float(msg_json["x"]), float(msg_json["y"]), float(msg_json["z"])) )

    def rolling_avg(self):
        total = [0,0,0]
        for v in self._buffer:
            for i in range(3):
                total[i] += float(v[i])

        return (total[0] / len(self._buffer),
                total[1] / len(self._buffer),
                total[2] / len(self._buffer))

    def __repr__(self):
        if len(self._buffer) > 0:
            v = self._buffer[-1]
            avg = self.rolling_avg()
            return self._name + "(raw: " + \
                "raw: ({:0.3f}, {:0.3f}, {:0.3f}) ".format(v[0],v[1],v[2]) + \
                "avg: ({:0.3f}, {:0.3f}, {:0.3f})".format(avg[0], avg[1], avg[2]) + \
                ")"

        return self._name + "()"
