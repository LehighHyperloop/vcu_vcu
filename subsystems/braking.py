from .subsystem import Subsystem

RELAY_BRAKING = 2

class Braking(Subsystem):
    _name = "braking"

    def simulate(self):
        pass

    ### LOGIC ###
    def off_func(self, t):
        if t == "ON":
            if self.hw_map["yun1"].set_remote_relay(RELAY_BRAKING, True):
                return "ON"
            return False
        return False

    def on_func(self, t):
        if t == "OFF":
            if self.hw_map["yun1"].set_remote_relay(RELAY_BRAKING, False):
                return "OFF"
            return False
        return False

    _states = {
        "OFF": off_func,
        "ON": on_func,
        "FAULT": None,
        "ESTOP": None
    }
    _default_state = "OFF"
