import json
import paho.mqtt.client as mqtt
import time
import string
import os
import subsystems

from command_handler import CommandHandler

# Setup client
client = mqtt.Client()
mqtt_IP = os.environ["MQTT_IP"]
client.connect(mqtt_IP, 1883)
client.loop_start()

# List subsystems
ss_map = {
    "braking": subsystems.Braking(client),
    "compressor": subsystems.Compressor(client),
    "fan": subsystems.Fan(client),
    "inverters": subsystems.Inverters(client),
    "levitation": subsystems.Levitation(client),
    "propulsion": subsystems.Propulsion(client),
    "wheels": subsystems.Wheels(client)
}
topic_to_ss = dict([ [ss.get_name(),ss] for key,ss in ss_map.iteritems() ])

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
        ss.handle_status_update(msg_json)

client.on_message = on_message

# Register to receive mqtt messages
client.subscribe("cmd")
for topic,ss in topic_to_ss.iteritems():
    client.subscribe(topic)

# Loop in main
try:
    while True:
        for name,ss in ss_map.iteritems():
            ss.send_target_state()
        for name,ss in ss_map.iteritems():
            # TODO: Make this more clear because this is very obtuse
            print name + "(" + \
                  string.join([ k + ": " + str(v) for k, v in ss.state().iteritems() ], ", ") + \
                  ") " + \
                  str(ss.last_update()) + "s"

        print ""
        time.sleep(0.1);

except KeyboardInterrupt:
    print("Shutting down...")
    print("Done!")

client.loop_stop()
