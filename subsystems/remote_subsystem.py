from .subsystem import Subsystem

import json
import string

class Remote_Subsystem(Subsystem):
    _client = None
    hw_map = None

    _prefix = "remote_subsystem/"

    _states        = None
    _states_array  = None
    _default_state = None

    #local_t_state is set by us, t_state and state are determined by the remote subsystem
    _local_t_state = None
    _t_state = None
    _state   = None

    def __init__(self, client, hw_map):
        print "INIT " + self._name
        self._client = client
        self.hw_map = hw_map
        self._states_array = [ k for k,v in self._states.iteritems() ]

        self._local_t_state = self._default_state
        self._t_state = self._default_state
        self._state = self._default_state

    def get_attributes(self):
        return {
            "local_t_state": self._local_t_state,
            "t_state": self._t_state,
            "state": self._state
        }

    #just periodically send your status so the state maintainer (which listens
    #on remote_subsystem/suspension) can handle the state transitions requested
    def update(self):
        self.send_action_set()

    def set_target_state(self, target):
        if target in self._states:
            self._local_t_state = target
        else:
            print "Unrecognized state: " + target_state

    def send_action_set(self):
        self._client.publish(self._prefix + self._name + "/set", json.dumps({
            "t_state": self._local_t_state
        }))

    def __repr__(self):
        return self._name + "(" + \
            string.join([ k + ": " + str(v) for k, v in self.get_attributes().iteritems() ], ", ") + \
            ")"
