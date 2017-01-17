import json
import string
import datetime

# Constants
RELAY_LEVITATION        = 0
RELAY_AUX_WHEELS        = 1
RELAY_BRAKING           = 2
RELAY_VFD_ENABLE        = 4
RELAY_COMPRESSOR_START  = 5
RELAY_COMPRESSOR_ENABLE = 6

class Yun1():
    _name = "arduino-yun1"
    _client = None

    def __init__(self, client):
        self._client = client

    def get_topic(self):
        return "remote/" + self._name

    # Internal State
    _local_state = {
        "relays": [False, False, False, False, False, False, False, False]
    }
    _remote_state = {
        "t": "",
        "relays": [False, False, False, False, False, False, False, False]
    }

    def set_relay(self, pin, value):
        self._local_state["relays"][pin] = value

    def get_relay(self, pin):
        return self._remote_state["relays"][pin]

    def set_remote_relay(self, pin, value):
        self.set_relay(pin, value)
        return self.get_relay(pin) == value

    # Serialization
    def add_timestamp_to_state(self, state):
        state.update({ "t": datetime.datetime.now().strftime("%s.%f") })
        return state

    def serialize_state(self, state):
        serialized = {}

        if "t" in state:
            serialized["t"] = state["t"]

        if "relays" in state:
            serialized["relays"] = string.join([ "1" if v else "0" for v in state["relays"]], "")

        return serialized

    def deserialize_state(self, serialized):
        state = {}

        if "t" in serialized:
            state["t"] = serialized["t"]

        if "relays" in serialized:
            state["relays"] = []
            for v in serialized["relays"]:
                state["relays"].append((v == "1"))

        return state

    def get_local_state(self):
        return self.serialize_state(self._local_state)

    def get_remote_state(self):
        return self.serialize_state(self._remote_state)

    # Communication
    _last_update = None

    def send_sync(self):
        state = self.get_local_state()
        state = self.add_timestamp_to_state(state)
        self._last_update = state["t"]
        self._client.publish(self.get_topic() + "/set",
                json.dumps(state))

    def handle_status_update(self, msg_json):
        self._remote_state = self.deserialize_state(msg_json)

    def last_update(self):
        return self._last_update

    def sync_diff(self):
        if self._remote_state["t"] == "":
            return -1
        return float(self.last_update()) - float(self._remote_state["t"])


    def __repr__(self):
        return self._name + "(" + \
            string.join([ k + ": " + str(v) for k, v in self.get_remote_state().iteritems() ], ", ") + \
            ") " + str(self.last_update()) + " ({:0.4f})".format(self.sync_diff())
