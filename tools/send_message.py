from app.config import Config
from app.communication.tcp_esp32 import TcpESP32

config = Config().communication
client = TcpESP32(config)

# Connect once at the start; the connection stays open for all messages

client.connect()

try:

    while True:
        text = input("bin (q = quit): ").strip()
        if text == "q":
            break
        # send() closes the connection on error, so reconnect if needed
        if client.connection is None:
            print("Connection lost, reconnecting...")
            if not client.connect():
                continue

        if (len(text) > 0 ):
            message = client.build_message(int(text))
            client.send(message)
            print("sent:", message)
except (KeyboardInterrupt, EOFError):
    pass
finally:
    client.close()
    print("connection closed")
