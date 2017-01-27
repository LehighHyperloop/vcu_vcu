import socket
import string
import struct

SPACEX_TELEMETRY_IP = "192.168.0.1"
SPACEX_TELEMETRY_PORT = 3000

class SpaceXTelemetryFrame():
    # team_id		UINT8	Identifier for the team, assigned by SpaceX. Required.
    # status		UINT8	Pod status, indicating current pod health and pushing state, as defined below. Required.
    # acceleration		INT32	Acceleration in centimeters per second squared. Required.
    # position		INT32	Velocity in centimeters per second. Required.
    # velocity		INT32	Position in centimeters. Required.
    # battery_voltage	INT32	Battery voltage in millivolts.
    # battery_current	INT32	Battery current in milliamps.
    # battery_temperature	INT32	Battery temperature in tenths of a degree Celsius.
    # pod_temperature	INT32 	Pod temperature in tenths of a degree Celsius.
    # stripe_count		UINT32	Count of optical navigation stripes detected in the tube._

    # Attributes
    team_id             = 19 # Lehigh team id
    status              = 0
    acceleration        = 0
    position            = 0
    velocity            = 0
    battery_voltage     = 0
    battery_current     = 0
    battery_temperature = 0
    pod_temperature     = 0
    stripe_count        = 0

    def pack(self):
        return struct.pack("!BBiiiiiiiI",
                self.team_id,
                self.status,
                self.acceleration,
                self.position,
                self.velocity,
                self.battery_voltage,
                self.battery_current,
                self.battery_temperature,
                self.pod_temperature,
                self.stripe_count)

    def get_attributes(self):
        return {
            "team_id": self.team_id,
            "status": self.status,
            "acceleration": self.acceleration,
            "position": self.position,
            "velocity": self.velocity,
            "battery_voltage": self.battery_voltage,
            "battery_current": self.battery_current,
            "battery_temperature": self.battery_temperature,
            "pod_temperature": self.pod_temperature,
            "stripe_count": self.stripe_count,
        }

class SpaceXTelemetry():
    _name = "spacex_telemetry"
    _global_state = None
    _sensor_map = None

    _last_frame = None

    def __init__(self, global_state, sensor_map):
        self._global_state = global_state
        self._sensor_map = sensor_map
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_heartbeat(self):
        frame = self.build_frame()
        self.send_frame(frame)
        self._last_frame = frame

    def build_frame(self):
        frame = SpaceXTelemetryFrame()

        frame.status = self._global_state.get_telemetry_status()
        x,y,z = self._sensor_map["accel"].rolling_avg()
        frame.acceleration = z * 100 # Convert from m/s^2 to cm/s^2
        # TODO: set other frame variables

        return frame

    def send_frame(self, frame):
        try:
            self._sock.sendto(frame.pack(), (SPACEX_TELEMETRY_IP, SPACEX_TELEMETRY_PORT))
        except:
            print "Failed to send telemetry frame"

    def __repr__(self):
        return self._name + "(" + \
            string.join([ k + ": " + str(v) for k,v in self._last_frame.get_attributes().iteritems() ], ", ") + \
            ")"


