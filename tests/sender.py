import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
USERNAME = ""
PASSWORD = ""

client = mqtt.Client()

client.username_pw_set(USERNAME, PASSWORD)

client.connect(BROKER, PORT)

client.publish("test/message", "Hello from Python!")

client.disconnect()