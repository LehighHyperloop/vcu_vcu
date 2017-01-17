from .subsystem import Subsystem

RELAY_VFD_ENABLE        = 4
RELAY_COMPRESSOR_START  = 5
RELAY_COMPRESSOR_ENABLE = 6

class Compressor(Subsystem):
    _name = "compressor"

    ### LOGIC ###
    def stopped_func(hw_map, t):
        if t == "RUNNING":
            if hw_map["yun1"].set_remote_relay(RELAY_VFD_ENABLE, True):
                return "VFD_STARTING"
            return False
        return False

    def vfd_starting_func(hw_map, t):
        if t == "RUNNING":
            if hw_map["yun1"].set_remote_relay(RELAY_COMPRESSOR_ENABLE, True):
                return "COMPRESSOR_STARTING"
            return False
        return False

    def compressor_starting_func(hw_map, t):
        if t == "RUNNING":
            if hw_map["yun1"].set_remote_relay(RELAY_COMPRESSOR_START, True):
                return "RUNNING"
            return False
        return False

    def running_func(hw_map, t):
        # Turn off momentary start button
        hw_map["yun1"].set_remote_relay(RELAY_COMPRESSOR_START, False)
        if t == "STOPPED":
            return "COMPRESSOR_STOPPING"
        return False

    def compressor_stopping_func(hw_map, t):
        if t == "STOPPED":
            if hw_map["yun1"].set_remote_relay(RELAY_COMPRESSOR_ENABLE, False):
                return "VFD_STOPPING"
            return False
        return False

    def vfd_stopping_func(hw_map, t):
        if t == "STOPPED":
            if hw_map["yun1"].set_remote_relay(RELAY_VFD_ENABLE, False):
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
