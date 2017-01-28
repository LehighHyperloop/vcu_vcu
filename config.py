import json

class Config():
    _client = None

    _config = {}

    def __init__(self, client):
        self._client = client
        self.load()

    def load(self, config_name = "config.json"):
        try:
            with open(config_name) as f:
                data = json.load(f)
                self._config = data

                s = ""

                for k,v in self._config.iteritems():
                    s += str(k) + ": " + str(v) + "\n"

                self._client.debug("Successfully loading config!\n\n" + s)
        except Exception as e:
            self._client.debug("Error loading config file! " + str(e))

    def get(self, key):
        return self._config[key]

