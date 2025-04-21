import paho.mqtt.client as mqtt

# MQTT configuration
BROKER_ADDRESS = "8.222.194.160"
PORT = 1883
USERNAME = "cshwstem"
PASSWORD = "Cshw0918#"
TOPIC = "/mqtt/node"

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Successfully connected to MQTT broker.")
        client.subscribe(TOPIC)
        print(f"📡 Subscribed to topic: {TOPIC}")
    else:
        print(f"❌ Failed to connect, return code: {rc}")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        print(f"📥 Received message: {payload}")
    except Exception as e:
        print(f"⚠️ Failed to decode message: {e}")

# Initialize MQTT client
client = mqtt.Client()

# Set username and password
client.username_pw_set(USERNAME, PASSWORD)

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
print("🔌 Attempting to connect to MQTT broker...")
client.connect(BROKER_ADDRESS, PORT, 60)

# Start the network loop to process incoming and outgoing messages
client.loop_forever()
