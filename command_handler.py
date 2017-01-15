import string

class CommandHandler:
    def __init__(self, ss_map):
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
