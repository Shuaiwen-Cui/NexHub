import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import paho.mqtt.client as mqtt

# Flask setup
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# MQTT Configuration
BROKER_ADDRESS = "8.222.194.160"
PORT = 1883
USERNAME = "cshwstem"
PASSWORD = "Cshw0918#"
TOPIC = "/mqtt/node"

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("MQTT Connected with result code " + str(rc))
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    try:
        # Extract data using string parsing
        parts = payload.split(',')
        time_stamp = parts[0].split(':')[1].strip()
        acc_x = float(parts[1].split('=')[1])
        acc_y = float(parts[2].split('=')[1])
        acc_z = float(parts[3].split('=')[1])
        temperature = float(parts[4].split(':')[1].split()[0])

        # Emit to web frontend via SocketIO
        socketio.emit('sensor_data', {
            'time': time_stamp,
            'acc_x': acc_x,
            'acc_y': acc_y,
            'acc_z': acc_z,
            'temperature': temperature
        })
    except Exception as e:
        print(f"Parse error: {e}")

# Start MQTT client in background
def mqtt_thread():
    client = mqtt.Client()
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_ADDRESS, PORT, 60)
    client.loop_forever()

# Web route
@app.route('/')
def index():
    return render_template('index.html')

# Run app
if __name__ == '__main__':
    socketio.start_background_task(mqtt_thread)
    socketio.run(app, host='0.0.0.0', port=5000)
