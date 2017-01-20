from .remote_subsystem import Remote_Subsystem


class Suspension(Remote_Subsystem):
    _name = "suspension"

    # def idle_func(t):
    #     if t == "READY":
    #         if "some_controller" in hw_map:
    #             if hw_map["some_controller"].change_state():
    #                 return "HOMING"
    #             return False
    #         return False
    #     return False
    #
    # def homing_func(t):
    #     if t == "READY":
    #         if "some_controller" in hw_map:
    #             if hw_map["some_controller"].change_state():
    #                 return "READY"
    #             return False
    #         return False
    #     return False
    #
    # def ready_func(t):
    #     if t == "RUNNING":
    #         if "some_controller" in hw_map:
    #             if hw_map["some_controller"].change_state():
    #                 return "RUNNING"
    #             return False
    #         return False
    #     return False
    #
    # def running_func(t):
    #     if t == "READY":
    #         if "some_controller" in hw_map:
    #             if hw_map["some_controller"].change_state():
    #                 return "READY"
    #             return False
    #         return False
    #     elif t == "RUNNING_AND_LOGGING":
    #         if "some_controller" in hw_map:
    #             if hw_map["some_controller"].change_state():
    #                 return "RUNNING_AND_LOGGING"
    #             return False
    #         return False
    #     return False
    #
    # def running_and_logging_func(t):
    #     if t == "READY":
    #         if "some_controller" in hw_map:
    #             if hw_map["some_controller"].change_state():
    #                 return "READY"
    #             return False
    #         return False
    #     elif t == "RUNNING":
    #         if "some_controller" in hw_map:
    #             if hw_map["some_controller"].change_state():
    #                 return "RUNNING"
    #             return False
    #         return False
    #     return False


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
