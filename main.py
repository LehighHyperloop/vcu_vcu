import json
import paho.mqtt.client as mqtt
import time
import string
import os

from command_handler import CommandHandler

# Setup client
client = mqtt.Client()
mqtt_IP = os.environ["MQTT_IP"]
client.connect(mqtt_IP, 1883)
client.loop_start()

import hardware
hw_map = {
    "yun1": hardware.Yun1(client)
}

import subsystems
ss_map = {
    "compressor": subsystems.Compressor(client),
    "fan": subsystems.Fan(client),
    "levitation": subsystems.Levitation(client),
    "propulsion": subsystems.Propulsion(client),
    "inverters": subsystems.Inverters(client),
    "braking": subsystems.Braking(client)
}

topic_to_handler = {}

for _,klass in hw_map.iteritems():
    topic_to_handler[klass.get_topic()] = klass

# Handle messages
command_handler = CommandHandler(ss_map)
def on_message(mosq, obj, msg):
    if msg.topic == "cmd":
        command_handler.cmd(msg.payload)
        return

    msg_json = json.loads(msg.payload)

    handler = topic_to_handler[msg.topic]
    if handler is None:
        print "NOT MAPPED " + msg.topic
    else:
        handler.handle_status_update(msg_json)

client.on_message = on_message

# Register to receive mqtt messages
client.subscribe("cmd")
for topic,_ in topic_to_handler.iteritems():
    client.subscribe(topic)

# Loop in main
try:
    while True:
        # Update subsystems
        for name,ss in ss_map.iteritems():
            ss.update()

        # Send updates to hardware
        for name,hw in hw_map.iteritems():
            hw.send_sync()

        # Debug
        for name,hw in hw_map.iteritems():
            print hw
        for name,ss in ss_map.iteritems():
            print ss

        print ""

        time.sleep(0.1);

except KeyboardInterrupt:
    print("Shutting down...")
    print("Done!")

client.loop_stop()
