from .subsystem import Subsystem

RELAY_FAN_ENABLE = 7

class Fan(Subsystem):
    _name = "fan"

    ### LOGIC ###
    def stopped_func(self, t):
        if t == "RUNNING":
            # Wait for pin to be set
            if self.hw_map["yun1"].set_remote_relay(RELAY_FAN_ENABLE, True):
                return "RUNNING"
            return False
        return False

    def running_func(self, t):
        if t == "STOPPED":
            if self.hw_map["yun1"].set_remote_relay(RELAY_FAN_ENABLE, False):
                return "STOPPED"
            return False
        return False

    _states = {
        "STOPPED": stopped_func,
        "RUNNING": running_func,
        "FAULT": None,
        "ESTOP": None
    }
    _default_state = "STOPPED"
