import time
import json

class Subsystem():
    _client = None

    _prefix = "subsystem/"

    _states = []

    _current_state = None
    _target_state  = None
    _last_update   = -1

    def __init__(self, client):
        print "INIT " + self.get_name()
        self._client = client
        self._current_state = self._states[0]
        self._target_state  = self._states[0]

    def __init_complete__(self):
        print "DONE " + self.get_name()

    def get_name(self):
        return self._prefix + self._name

    def handle_status_update(self, msg_json):
        self._last_update = time.time()
        self._current_state = msg_json["state"]
        self._target_state = msg_json["t_state"]

    def state(self):
        return {
            "state": self._current_state,
            "target_state": self._target_state
        }

    def last_update(self):
        if self._last_update == -1:
            return -1
        return time.time() - self._last_update

    def send_action(self, action, msg):
        self._client.publish( \
            self.get_name() + "/" + action, \
            json.dumps(msg))

    def set_target_state(self, target_state):
        if target_state in self._states:
            self._target_state = target_state
            self.send_action("set", { "t_state": target_state })
        else:
            print "Unrecognized state: " + target_state
