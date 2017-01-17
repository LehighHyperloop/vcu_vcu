import json
import string

class Subsystem():
    _client = None
    hw_map = None

    _prefix = "subsystem/"

    _states        = None
    _states_array  = None
    _default_state = None

    _t_state = None
    _state   = None

    def __init__(self, client, hw_map):
        print "INIT " + self._name
        self._client = client
        self.hw_map = hw_map
        self._states_array = [ k for k,v in self._states.iteritems() ]

        self._t_state = self._default_state
        self._state = self._default_state

    def get_attributes(self):
        return {
            "t_state": self._t_state,
            "state": self._state
        }

    def state_transitions(self, current, target):
        func = self._states[current]
        if func:
            new = func(self.hw_map, target)
            if new == False:
                print("Error switching from " + current + " to " + target)
                return False
            return new
        return False

    def update(self):
        new_state = self.state_transitions(self._state, self._t_state)
        if new_state:
            self._state = new_state
            self.send_heartbeat()

    def set_target_state(self, target_state):
        if target_state in self._states:
            self._t_state = target_state
        else:
            print "Unrecognized state: " + target_state

    def send_heartbeat(self):
        # Send status updates
        self._client.publish(self._prefix + self._name, json.dumps(self.get_attributes()))

    def __repr__(self):
        return self._name + "(" + \
            string.join([ k + ": " + str(v) for k, v in self.get_attributes().iteritems() ], ", ") + \
            ")"
