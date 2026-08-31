import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
USERNAME = ""
PASSWORD = ""


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe("test/message")


def on_message(client, userdata, msg):
    print(f"Received: {msg.payload.decode()}")


client = mqtt.Client()

client.username_pw_set(USERNAME, PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

client.loop_forever()