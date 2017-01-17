from .subsystem import Subsystem

class Compressor(Subsystem):
    _name = "compressor"

    ### LOGIC ###
    def stopped_func(hw_map, t):
        if t == "RUNNING":
            return "VFD_STARTING"
        return False

    def vfd_starting_func(hw_map, t):
        if t == "RUNNING":
            return "COMPRESSOR_STARTING"
        return False

    def compressor_starting_func(hw_map, t):
        if t == "RUNNING":
            return "RUNNING"
        return False

    def running_func(hw_map, t):
        if t == "STOPPED":
            return "COMPRESSOR_STOPPING"
        return False

    def compressor_stopping_func(hw_map, t):
        if t == "STOPPED":
            return "VFD_STOPPING"
        return False

    def vfd_stopping_func(hw_map, t):
        if t == "STOPPED":
            return "STOPPED"
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
