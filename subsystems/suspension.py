from .remote_subsystem import Remote_Subsystem


class Suspension(Remote_Subsystem):
    _name = "suspension"


    #NOTE: these state transitions are very half-assed because
    #my brain is fried and we aren't entirely sure what the
    #inputs will look like that actually control this in the hardware
    def idle_func(t):
        if t == "HOMING":
            if "some_controller" in hw_map:
                if hw_map["some_controller"].change_state():
                    return "HOMING"
                return False
            return False
        return False

    def homing_func(t):
        if t == "READY":
            if "some_controller" in hw_map:
                if hw_map["some_controller"].change_state():
                    return "READY"
                return False
            return False
        return False

    def ready_func(t):
        if t == "RUNNING":
            if "some_controller" in hw_map:
                if hw_map["some_controller"].change_state():
                    return "RUNNING"
                return False
            return False
        return False

    def running_func(t):
        if t == "READY":
            if "some_controller" in hw_map:
                if hw_map["some_controller"].change_state():
                    return "READY"
                return False
            return False
        elif t == "RUNNING_AND_LOGGING":
            if "some_controller" in hw_map:
                if hw_map["some_controller"].change_state():
                    return "RUNNING_AND_LOGGING"
                return False
            return False
        return False

    def running_and_logging_func(t):
        if t == "READY":
            if "some_controller" in hw_map:
                if hw_map["some_controller"].change_state():
                    return "READY"
                return False
            return False
        elif t == "RUNNING":
            if "some_controller" in hw_map:
                if hw_map["some_controller"].change_state():
                    return "RUNNING"
                return False
            return False
        return False




    _states = {
        "IDLE": idle_func,
        "HOMING": homing_func,
        "READY": ready_func,
        "RUNNING": running_func,
        "RUNNING_AND_LOGGING": running_and_logging_func,
        "FAULT": None,
        "ESTOP": None,
    }
    _default_state = "IDLE"
