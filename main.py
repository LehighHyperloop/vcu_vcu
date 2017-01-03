import json
import paho.mqtt.client as mqtt
import time
import string

import subsystems

ss_map = {
    "compressor": subsystems.Compressor()
}

# Setup client
client = mqtt.Client()
client.connect("localhost", 1883)
client.loop_start()

_ss_map_mqtt = {}
def on_message(mosq, obj, msg):
    msg_json = json.loads(msg.payload)

    mapped_ss = _ss_map_mqtt[msg.topic]
    if not mapped_ss is None:
        mapped_ss.handle_status_update(msg_json)
    else:
        print "NOT MAPPED " + msg.topic

client.on_message = on_message

for name,ss in ss_map.iteritems():
    # Register to receive mqtt messages
    client.subscribe(ss.get_name())
    _ss_map_mqtt[ss.get_name()] = ss

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
