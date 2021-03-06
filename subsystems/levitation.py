from .subsystem import Subsystem

RELAY_LEVITATION = 0

class Levitation(Subsystem):
    _name = "levitation"

    def simulate(self):
        pass

    ### LOGIC ###
    def stopped_func(self, t):
        if t == "RUNNING":
            if self.hw_map["yun1"].set_remote_relay(RELAY_LEVITATION, True):
                return "RUNNING"
            return False
        return False

    def running_func(self, t):
        if t == "STOPPED":
            if self.hw_map["yun1"].set_remote_relay(RELAY_LEVITATION, False):
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
