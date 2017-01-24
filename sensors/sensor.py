class Sensor():
    _client = None

    _prefix = "sensor/"

    def __init__(self, client):
        self._client = client

    def get_topic(self):
        return self._prefix + self._location + "/" + self._name
