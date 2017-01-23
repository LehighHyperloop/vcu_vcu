from .subsystem import Subsystem

RELAY_LATERALCONTROL_EXTEND = 3
class LateralControl(Subsystem):
    _name = "lateral_control"

    ### LOGIC ###
    def extended_func(self, t):
        if t == "RETRACTED":
            if self.hw_map["yun1"].set_remote_relay(RELAY_LATERALCONTROL_EXTEND, True):
                return "RETRACTED"
            return False
        return False

    def retracted_func(self, t):
        if t == "EXTENDED":
            if self.hw_map["yun1"].set_remote_relay(RELAY_LATERALCONTROL_EXTEND, False):
                return "EXTENDED"
            return False
        return False

    _states = {
        "EXTENDED": extended_func,
        "RETRACTED": retracted_func,
        "FAULT": None,
        "ESTOP": None
    }
    _default_state = "extended_func"
