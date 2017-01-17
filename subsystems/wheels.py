from .subsystem import Subsystem

class Wheels(Subsystem):
    _name = "wheels"

    def simulate(self):
        pass

    ### LOGIC ###
    def up_func(hw_map, t):
        if t == "DOWN":
            return "DOWN"
        return False

    def down_func(hw_map, t):
        if t == "UP":
            return "UP"
        return False

    _states = {
        "UP": up_func,
        "DOWN": down_func,
        "FAULT": None,
        "ESTOP": None
    }
    _default_state = "UP"
