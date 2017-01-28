import string
import time

class CommandHandler:
    def __init__(self, global_state, ss_map):
        self.global_state = global_state
        self.ss_map = ss_map

    def cmd(self, msg_str):
        cmd_split = string.split(msg_str)
        if cmd_split[0] == "set":
            if cmd_split[1] in self.ss_map:
                target = self.ss_map[cmd_split[1]]
                state  = cmd_split[2]

                if target != None:
                    target.set_target_state(state)
            else:
                print "Unknown subsystem: " + cmd_split[1]
        elif cmd_split[0] == "set_global":
            if cmd_split[1] in self.global_state._states:
                self.global_state._state_entry_time = time.time()
                self.global_state._state = cmd_split[1]
            else:
                print "Unknown global state: " + cmd_split[1]
        elif cmd_split[0] == "ack":
            self.global_state.ack()
