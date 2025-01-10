import os
import sys
import paho.mqtt.client as mqtt
from flask import Flask, jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit
from datetime import datetime
from user_data import user_data  # Import user_data from user_data.py
import json
from flask_cors import CORS
import ssl
import logging

# MQTT Client setup
AWS_IOT_ENDPOINT = "a3lnnu1armgvqt-ats.iot.us-east-1.amazonaws.com"
AWS_THING_NAME = "gym_attendance_system"

# Paths to the certificate files
AWS_CA_CERT = "aws_ca_cert.pem"
AWS_CERT = "aws_cert.pem"       
AWS_PRIVATE_KEY = "aws_private_key.pem"  

TOPIC_USER_DETAILS = "/user_details"
TOPIC_CHECK_USER = "/check_user"
TOPIC_GYM_STATUS = "/gym_status"

# Global mqtt_client variable
mqtt_client = None
gym_status = "closed"  # Initial gym status

# Logging setup with a console handler
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler(sys.stdout)  # Sends logs to stdout
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Optionally, log to stderr for errors
error_handler = logging.StreamHandler(sys.stderr)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
logger.addHandler(error_handler)

sys.stdout.flush()  # Flush stdout immediately

def init_mqtt_client():
    global mqtt_client
    logger.debug("Initializing MQTT client...")
    mqtt_client = mqtt.Client()
    logger.debug("Setting up TLS with certificates...")
    try:
        mqtt_client.tls_set(
            ca_certs=AWS_CA_CERT,
            certfile=AWS_CERT,
            keyfile=AWS_PRIVATE_KEY,
            tls_version=ssl.PROTOCOL_TLSv1_2,
        )
        logger.info("TLS setup completed successfully.")
    except Exception as e:
        logger.error(f"Error setting up TLS: {e}")
        raise SystemExit("TLS setup failed. Exiting.")

    logger.info("Setting up callback functions...")
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    logger.info(f"Connecting to MQTT broker at {AWS_IOT_ENDPOINT} on port 8883...")
    try:
        mqtt_client.connect(AWS_IOT_ENDPOINT, port=8883, keepalive=60)
        logger.info(f"Successfully connected to MQTT broker at {AWS_IOT_ENDPOINT}.")
    except Exception as e:
        logger.error(f"Error connecting to MQTT broker: {e}")


# Callback functions for MQTT
def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected to AWS IoT Core with result code {rc}")
    client.subscribe(TOPIC_CHECK_USER)


def on_message(client, userdata, msg):
    logger.debug(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    message = json.loads(msg.payload.decode())
    card_id = message.get("card_id")
    if card_id:
        response_data = {}
        if not user_data.get(card_id):
            response_data["status"] = "not registered"
            client.publish(TOPIC_USER_DETAILS, json.dumps(response_data))
        else:
            user = user_data[card_id]
            if user.get("paidMembership"):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user["attendances"].append(timestamp)
                response_data["status"] = "valid"
                response_data["first_name"] = user["firstName"]
                response_data["attendances"] = len(user["attendances"])
            else:
                response_data["status"] = "invalid"
            client.publish(TOPIC_USER_DETAILS, json.dumps(response_data))


# Initialize MQTT client
init_mqtt_client()

if mqtt_client is None:
    logger.info("MQTT client initialization failed. Exiting.")
    exit(1)

mqtt_client.loop_start()

logger.info("MQTT client loop started.")

# Flask app setup
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing if needed
socketio = SocketIO(app)

@app.route('/')
def index():
    return jsonify({"message": "MQTT is running."})

@app.route('/send_message', methods=['POST'])
def send_message():
    content = request.json
    topic = content.get("topic")
    message = content.get("message")
    
    if topic and message:
        mqtt_client.publish(topic, message)
        return jsonify({"status": "success", "message": f"Message sent to {topic}."})
    else:
        return jsonify({"status": "error", "message": "Missing topic or message."}), 400

# WebSocket Example to receive messages from the frontend (optional)
@socketio.on('connect')
def handle_connect():
    emit("response", {"message": "Connected to WebSocket!"})

@socketio.on('send_message')
def handle_send_message(data):
    topic = data.get("topic")
    message = data.get("message")
    
    if topic and message:
        mqtt_client.publish(topic, message)
        emit("response", {"message": f"Message sent to {topic}."})
    else:
        emit("response", {"message": "Error: Missing topic or message."})

# Route to update gym status
@app.route("/api/update_gym_status", methods=["POST"])
def update_gym_status():
    global gym_status
    gym_status = request.json.get("gym_status")
    logger.info(f"Gym status updated to: {gym_status}")
    mqtt_client.publish(TOPIC_GYM_STATUS, json.dumps({"gym_status": gym_status}))
    return jsonify(
        {"message": "Gym status updated successfully", "gym_status": gym_status}
    )

if __name__ == '__main__':
    # Start the Flask server
    socketio.run(app, host='0.0.0.0', port=5000)
