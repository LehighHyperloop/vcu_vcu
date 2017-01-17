from .subsystem import Subsystem

class Fan(Subsystem):
    _name = "fan"

    ### LOGIC ###
    def stopped_func(t):
        if t == "RUNNING":
            return "RUNNING"
        return False

    def running_func(t):
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
