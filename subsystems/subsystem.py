import time

class Subsystem():
    _prefix = "subsystem/"

    _states         = {}
    _states_reverse = {}

    _current_state = 0
    _target_state  = 0
    _last_update   = -1

    def __init__(self):
        print "INIT " + self.get_name()
        # map states in reverse
        for k, v in self._states.iteritems():
            self._states_reverse[v] = k

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
