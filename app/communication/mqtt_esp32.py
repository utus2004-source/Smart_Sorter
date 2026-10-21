import paho.mqtt.client as mqtt
from .base import Communication


class MqttESP32(Communication):
    # Responsibilities:
    # - Connect to the MQTT broker
    # - Publish the bin number for the ESP32
    # - Close the connection

    def __init__(self, config):

        self.enabled = config["enabled"]
        self.broker = config["broker"]
        self.broker_port = config["broker_port"]
        self.topic = config["topic"]
        self.username = config["username"]
        self.password = config["password"]

        self.client = None

    def connect(self):

        # Communication can be switched off while testing on a laptop
        if not self.enabled:
            print("ESP32 communication is disabled.")
            return False

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        if self.username:
            client.username_pw_set(self.username, self.password)

        # Without a broker the pipeline keeps running, only nothing is sent
        try:
            client.connect(self.broker, self.broker_port)
        except OSError as error:
            print(f"Could not connect to MQTT broker {self.broker}:{self.broker_port}: {error}")
            return False

        # Network loop runs in the background and reconnects on its own
        client.loop_start()
        self.client = client

        print(f"MQTT connected to {self.broker}:{self.broker_port}, topic {self.topic}")

        return True

    def send(self, command):

        if self.client is None:
            return

        # Only the bin number is sent, qos=1 so the broker confirms delivery
        self.client.publish(self.topic, str(command), qos=1)

    def close(self):

        if self.client is not None:
            self.client.loop_stop()
            self.client.disconnect()
