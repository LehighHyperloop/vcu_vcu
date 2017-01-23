from .subsystem import Subsystem

RELAY_VFD_ENABLE        = 4
RELAY_COMPRESSOR_START  = 5
RELAY_COMPRESSOR_ENABLE = 6

class Compressor(Subsystem):
    _name = "compressor"

    ### LOGIC ###
    def stopped_func(self, t):
        if t == "RUNNING":
            if self.hw_map["yun1"].set_remote_relay(RELAY_VFD_ENABLE, True):
                return "VFD_STARTING"
            return False
        return False

    def vfd_starting_func(self, t):
        if t == "RUNNING":
            if self.time_in_state() >= 5 and \
               self.hw_map["yun1"].set_remote_relay(RELAY_COMPRESSOR_ENABLE, True):
                return "COMPRESSOR_STARTING"
            return False
        return False

    def compressor_starting_func(self, t):
        if t == "RUNNING":
            if self.time_in_state() >= 5 and \
               self.hw_map["yun1"].set_remote_relay(RELAY_COMPRESSOR_START, True):
                return "RUNNING"
            return False
        return False

    def running_func(self, t):
        # Turn off momentary start button
        self.hw_map["yun1"].set_remote_relay(RELAY_COMPRESSOR_START, False)
        if t == "STOPPED":
            return "COMPRESSOR_STOPPING"
        return False

    def compressor_stopping_func(self, t):
        if t == "STOPPED":
            if self.hw_map["yun1"].set_remote_relay(RELAY_COMPRESSOR_ENABLE, False):
                return "VFD_STOPPING"
            return False
        return False

    def vfd_stopping_func(self, t):
        if t == "STOPPED":
            if self.time_in_state() >= 10 and \
               self.hw_map["yun1"].set_remote_relay(RELAY_VFD_ENABLE, False):
                return "STOPPED"
            return False
        return False

    _states = {
        "STOPPED": stopped_func,
        "VFD_STARTING": vfd_starting_func,
        "COMPRESSOR_STARTING": compressor_starting_func,
        "RUNNING": running_func,
        "COMPRESSOR_STOPPING": compressor_stopping_func,
        "VFD_STOPPING": vfd_stopping_func,
        "FAULT": None,
        "ESTOP": None,
    }
    _default_state = "STOPPED"
