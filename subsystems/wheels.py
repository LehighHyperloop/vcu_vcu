from .subsystem import Subsystem

RELAY_AUX_WHEELS = 1

class Wheels(Subsystem):
    _name = "wheels"

    def simulate(self):
        pass

    ### LOGIC ###
    def up_func(self, t):
        if t == "DOWN":
            if self.hw_map["yun1"].set_remote_relay(RELAY_AUX_WHEELS, True):
                return "DOWN"
            return False
        return False

    def down_func(self, t):
        if t == "UP":
            if self.hw_map["yun1"].set_remote_relay(RELAY_AUX_WHEELS, False):
                return "UP"
            return False
        return False

    _states = {
        "UP": up_func,
        "DOWN": down_func,
        "FAULT": None,
        "ESTOP": None
    }
    _default_state = "UP"
