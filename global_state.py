import json
import string

ACK_NONE      = 0
ACK_REQUESTED = 1
ACK_GRANTED   = 2

SPACEX_FAULT   = 0 # If seen, will cause SpaceX to abort the tube run.
SPACEX_IDLE    = 1 # Any state where the pod is on, but not ready to be pushed.
SPACEX_READY   = 2 # Any state where the pod is ready to be pushed.
SPACEX_PUSHING = 3 # Any state when the pod detects it is being pushed.
SPACEX_COAST   = 4 # Any state when the pod detects it has separated from the pusher vehicle.
SPACEX_BRAKING = 5 # Any state when the pod is applying its brakes.


class GlobalState():
    _client = None
    ss_map = None
    sensor_map = None

    _name = "global_state"

    _state = None
    _first_state_run = True
    _current_blocker = None

    _telemetry_state = SPACEX_IDLE

    def __init__(self, client, ss_map, sensor_map):
        self._client = client
        self.ss_map = ss_map
        self.sensor_map = sensor_map
        self._state = self._default_state

    def update(self):
        # Run current state
        func = self._states[self._state]
        if func:
            self._current_blocker = None
            new = func(self, self._state)
            if new:
                self._client.debug("Transition " + self._name + " from " + self._state + " to " + new)
                self._state = new
                self._first_state_run = True
        else:
            print "ERROR FINDING STATE " + self._state

        self.send_heartbeat()

    def send_heartbeat(self):
        self._client.publish(self._name, json.dumps(self.get_attributes()))

    def get_attributes(self):
        return {
            "state": self._state,
            "current_blocker": self._current_blocker
        }

    _ack = ACK_NONE
    def need_ack(self):
        if self._ack == ACK_NONE:
            self._ack = ACK_REQUESTED
            self._current_blocker = "ack"
            return False

        if self._ack == ACK_GRANTED:
            self._ack = ACK_NONE
            return True

        # Ack is still requested but not yet granted
        self._current_blocker = "ack"
        return False

    def ack(self):
        if self._ack == ACK_REQUESTED:
            self._ack = ACK_GRANTED

    def state_init(self):
        return self._first_state_run

    def set_subsystem_target(self, ss, target):
        if self.ss_map[ss].get_state() == target:
            return True

        self.ss_map[ss].set_target_state(target)
        self._current_blocker = ss
        return False

    ### LOGIC ###
    def standby_func(self, t):
        self._telemetry_state = SPACEX_IDLE
        if self.need_ack():
            return "PRELAUNCH"
        return False

    def prelaunch_func(self, t):
        self._telemetry_state = SPACEX_IDLE
        # TODO:
        # - Master & Slave inverter output wattage balanced
        # - Levitation Air Tank >= 100 psi
        # - Pneumatic Air tank >= 100 psi
        # - Receive manual transition command from operators
        #if self.set_subsystem_target("wheels", "UP") and \
        #   self.set_subsystem_target("suspension", "RUNNING") and \
        #   self.set_subsystem_target("inverters", "RUNNING") and \
        #   self.set_subsystem_target("lateralcontrol", "RUNNING") and \
        if self.set_subsystem_target("fan", "RUNNING") and \
           self.set_subsystem_target("compressor", "RUNNING") and \
           self.set_subsystem_target("propulsion", "STOPPED") and \
           self.set_subsystem_target("braking", "OFF") and \
           self.need_ack():
            return "LAUNCH"
        return False

    def launch_func(self, t):
        self._telemetry_state = SPACEX_READY
        if self.sensor_map["accel"].rolling_avg() >= 0.2 * 9.8 and \
           self.need_ack():
            return "PUSHING"
        return False

    def pushing_func(self, t):
        self._telemetry_state = SPACEX_PUSHING
        # TODO:
        # - Pod position > 1600ft
        # - Time in pushing state > PUSHING_TIME_AT_MAX_ACCELERATION (TBD, waiting on mechanical team)
        if self.set_subsystem_target("propulsion", "RUNNING") and \
           self.need_ack():
            return "PASTPUSHER"
        return False

    def pastpusher_func(self, t):
        self._telemetry_state = SPACEX_COAST
        # TODO:
        # - Pod position >= COAST_DISTANCE (TBD)
        if self.need_ack():
            return "COASTING"
        return False

    def coasting_func(self, t):
        self._telemetry_state = SPACEX_COAST
        # TODO:
        # - Pod position >= WHEEL_BRAKING_DISTANCE (TBD, estimated 1000ft from end of track, waiting on mechanical team)
        if self.set_subsystem_target("propulsion", "STOPPED") and \
           self.need_ack():
            return "WHEEL_BRAKING"
        return False

    def wheel_braking_func(self, t):
        self._telemetry_state = SPACEX_BRAKING
        # TODO:
        # - Set Propulsion: BRAKING
        # - Pod position >= FRICTION_BRAKING_DISTANCE (TBD, estimated 400ft from end of track, waiting on mechanical team)
        if self.need_ack():
            return "FRICTION_BRAKING"
        return False

    def friction_braking_func(self, t):
        self._telemetry_state = SPACEX_BRAKING
        # TODO:
        # - Pod Velocity == 0
        if self.set_subsystem_target("braking", "ON") and \
           self.need_ack():
            return "STOPPED"
        return False

    def stopped_func(self, t):
        self._telemetry_state = SPACEX_BRAKING
        if self.need_ack():
            return "DISENGAGED"
        return False

    def disengaged_func(self, t):
        self._telemetry_state = SPACEX_IDLE
        self.set_subsystem_target("levitation", "STOPPED") and \
        self.set_subsystem_target("braking", "OFF") and \
        self.set_subsystem_target("compressor", "STOPPED") and \
        self.set_subsystem_target("fan", "STOPPED")
        return False

    _states = {
        "STANDBY": standby_func,
        "PRELAUNCH": prelaunch_func,
        "LAUNCH": launch_func,
        "PUSHING": pushing_func,
        "PASTPUSHER": pastpusher_func,
        "COASTING": coasting_func,
        "WHEEL_BRAKING": wheel_braking_func,
        "FRICTION_BRAKING": friction_braking_func,
        "STOPPED": stopped_func,
        "DISENGAGED": disengaged_func,
        "FAULT": None,
        "ESTOP": None
    }
    _default_state = "STANDBY"

    # Telemetry functions
    def get_telemetry_status(self):
        return self._telemetry_state

    def __repr__(self):
        return self._name + "(" + \
            string.join([ k + ": " + str(v) for k, v in self.get_attributes().iteritems() ], ", ") + \
            ")"
