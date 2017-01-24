import time

class Sensor():
    _client = None

    _prefix = "sensor/"

    def __init__(self, client):
        self._client = client

    def get_topic(self):
        return self._prefix + self._location + "/" + self._name

    _last_update = None
    def last_update(self):
        if self._last_update:
            return time.time() - self._last_update
        return -1
