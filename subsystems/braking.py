from .subsystem import Subsystem

class Braking(Subsystem):
    _name = "braking"

    def simulate(self):
        pass

    ### LOGIC ###
    def off_func(hw_map, t):
        if t == "ON":
            return "ON"
        return False

    def on_func(hw_map, t):
        if t == "OFF":
            return "OFF"
        return False

    _states = {
        "OFF": off_func,
        "ON": on_func,
        "FAULT": None,
        "ESTOP": None
    }
    _default_state = "OFF"
