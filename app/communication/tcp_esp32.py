from .base import Communication
import socket

class TcpESP32(Communication):
    # Responsibilities:
    # - Connect to ESP32 
    # - Send a ready command
    # - Receive an ACK from ESP32 (to add !)
    # - Close the connection

    def __init__(self, config):

        self.enabled = config["enabled"]
        self.port = config["esp32_port"]
        self.host = config["esp32_host"]
        self.baudrate = config["baudrate"]
        self.connection_timeout = config["timeout"]
        self.connection = None

    def connect(self):

        # Communication can be switched off while testing on a laptop
        if not self.enabled:
            print("ESP32 communication is disabled.")
            return False

        #Try connecting to the Host
        try : 
            self.connection =   self.connection = socket.create_connection((self.host, self.port),self.connection_timeout)
        except  OSError as error:
            print (f"Could not connect to host with IP {self.host} on port {self.port} it erro is :{error}") 
            return False


        print(f"{self.host} is connected on port {self.port}") 
        return True

    def send(self, command):

        if self.connection is None:
            return

        command = "Ziorbo przestań mi rodzine prześladować :)"
        try:
            self.connection.sendall(f"{command}\n".encode())
        except OSError as error:
        
            print(f"Could not send command to ESP32: {error}")
            self.close()



    def close(self):

        if self.connection is not None:
            self.connection.close()
            self.connection = None