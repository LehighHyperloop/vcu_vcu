from .subsystem import Subsystem

class Propulsion(Subsystem):
    _name = "propulsion"

    def simulate(self):
        pass

    ### LOGIC ###
    def stopped_func(self, t):
        if t == "RUNNING":
            return "RUNNING"
        return False

    def running_func(self, t):
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
