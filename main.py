import json
import paho.mqtt.client as mqtt
import time
import string

import subsystems

from command_handler import CommandHandler

# Setup client
client = mqtt.Client()
client.connect("localhost", 1883)
client.loop_start()

# List subsystems
ss_map = {
    "compressor": subsystems.Compressor(client)
}
topic_to_ss = [ ss.get_name() for key,ss in ss_map.iteritems() ]

# Handle messages
command_handler = CommandHandler(ss_map)
def on_message(mosq, obj, msg):
    if msg.topic == "cmd":
        command_handler.cmd(msg.payload)
        return

    msg_json = json.loads(msg.payload)

    ss = topic_to_ss[msg.topic]
    if ss is None:
        print "NOT MAPPED " + msg.topic
    else:
        mapped_ss.handle_status_update(msg_json)

client.on_message = on_message

# Register to receive mqtt messages
client.subscribe("cmd")
for name,ss in ss_map.iteritems():
    client.subscribe(ss.get_name())

# Loop in main
try:
    while True:
        for name,ss in ss_map.iteritems():
            # TODO: Make this more clear because this is very obtuse
            print name + "(" + \
                  string.join([ k + ": " + str(v) for k, v in ss.state().iteritems() ], ", ") + \
                  ") " + \
                  str(ss.last_update()) + "s"

        time.sleep(0.1);

except KeyboardInterrupt:
    print("Shutting down...")
    print("Done!")

client.loop_stop()
