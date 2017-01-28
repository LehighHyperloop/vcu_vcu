import json
import paho.mqtt.client as mqtt
import time
import string
import os

from command_handler import CommandHandler
from global_state import GlobalState
from spacex_telemetry import SpaceXTelemetry
from config import Config

# Setup client
client = mqtt.Client()
mqtt_IP = os.environ["MQTT_IP"]
client.connect(mqtt_IP, 1883)
client.loop_start()

# Add debug to mqtt
def debug(msg):
    client.publish("debug/vcu", msg)

client.debug = debug

client.debug("INIT...")

config = Config(client)

import hardware
hw_map = {
    "yun1": hardware.Yun1(client)
}

import subsystems
ss_map = {
    "compressor": subsystems.Compressor(client, hw_map),
    "fan": subsystems.Fan(client, hw_map),
    "lateral_control": subsystems.LateralControl(client, hw_map),
    "levitation": subsystems.Levitation(client, hw_map),
    "propulsion": subsystems.Propulsion(client, hw_map),
    #"inverters": subsystems.Inverters(client, hw_map),
    "braking": subsystems.Braking(client, hw_map),
    "wheels": subsystems.Wheels(client, hw_map),
    "suspension": subsystems.Suspension(client, hw_map)
}

import sensors
sensor_map = {
    "accel": sensors.Accel(client),
    "pressure": sensors.Pressure(client),
    "rotation": sensors.Rotation(client),
    "suspension_accel": sensors.SuspensionAccel(client),
    "suspension_distance": sensors.SuspensionDistance(client)
}

global_state = GlobalState(client, config, ss_map, sensor_map)
spacex_telemetry = SpaceXTelemetry(global_state, sensor_map)

topic_to_handler = {}

for _,klass in hw_map.iteritems():
    topic_to_handler[klass.get_topic()] = klass
for _,klass in ss_map.iteritems():
    if klass.get_topic():
        topic_to_handler[klass.get_topic()] = klass
for _,klass in sensor_map.iteritems():
    if klass.get_topic():
        topic_to_handler[klass.get_topic()] = klass


# Handle messages
command_handler = CommandHandler(global_state, ss_map, config)
def on_message(mosq, obj, msg):
    try:
        if msg.topic == "cmd":
            command_handler.cmd(msg.payload)
            return

        msg_json = json.loads(msg.payload)

        handler = topic_to_handler[msg.topic]
        if handler is None:
            print "NOT MAPPED " + msg.topic
        else:
            handler.handle_status_update(msg_json)
    except:
        print "error on_message: " + msg.topic + ": " + msg.payload

client.on_message = on_message

# Register to receive mqtt messages
client.subscribe("cmd")
for topic,_ in topic_to_handler.iteritems():
    client.subscribe(topic)

client.debug("INIT COMPLETE")

# Loop in main
try:
    while True:
        # Update global state
        global_state.update()

        # Send telemetry
        spacex_telemetry.send_heartbeat()

        # Update subsystems
        for name,ss in ss_map.iteritems():
            ss.update()

        # Send updates to hardware
        for name,hw in hw_map.iteritems():
            hw.send_sync()

        # Debug
        try:
            print global_state
            print spacex_telemetry
            for name,hw in hw_map.iteritems():
                print hw
            for name,ss in ss_map.iteritems():
                print ss
            for name,sensor in sensor_map.iteritems():
                print sensor
        except:
            print "Error in debug"

        print ""

        time.sleep(0.1);

except KeyboardInterrupt:
    print("Shutting down...")
    print("Done!")

client.loop_stop()
