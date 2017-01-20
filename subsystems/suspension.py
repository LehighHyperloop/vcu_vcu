from .remote_subsystem import Remote_Subsystem


class Suspension(Remote_Subsystem):
    _name = "suspension"


    #remote subsystems don't have to manage their own state
    _states = {
        "IDLE": None,
        "HOMING": None,
        "READY": None,
        "RUNNING": None,
        "RUNNING_AND_LOGGING": None,
        "FAULT": None,
        "ESTOP": None,
    }
    _default_state = "IDLE"
