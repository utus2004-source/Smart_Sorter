import serial
from .base import Communication


class SerialESP32(Communication):
    # Responsibilities:
    # - Open the serial connection to the ESP32
    # - Send a ready command
    # - Close the connection

    def __init__(self, config):

        self.enabled = config["enabled"]
        self.port = config["port"]
        self.baudrate = config["baudrate"]

        self.connection = None

    def connect(self):

        # Communication can be switched off while testing on a laptop
        if not self.enabled:
            print("ESP32 communication is disabled.")
            return False

        self.connection = serial.Serial(
            self.port,
            self.baudrate,
            timeout=1
        )

        print(f"ESP32 connected on {self.port}")

        return True

    def send(self, command):

        if self.connection is None:
            return

        # The command is sent as a single line of text
        self.connection.write(f"{command}\n".encode())

    def close(self):

        if self.connection is not None:
            self.connection.close()
