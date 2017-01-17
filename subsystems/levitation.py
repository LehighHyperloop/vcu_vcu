from .subsystem import Subsystem

class Levitation(Subsystem):
    _name = "levitation"

    def simulate(self):
        pass

    ### LOGIC ###
    def stopped_func(hw_map, t):
        if t == "RUNNING":
            return "RUNNING"
        return False

    def running_func(hw_map, t):
        if t == "STOPPED":
            return "STOPPED"
        return False

    _states = {
        "STOPPED": stopped_func,
        "RUNNING": running_func,
        "FAULT": None,
        "ESTOP": None
    }
    _default_state = "STOPPED"
