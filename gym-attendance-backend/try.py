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


# Function to print certificate contents
def print_cert_content(cert_file):
    try:
        with open(cert_file, "r") as file:
            cert_content = file.read()
            logger.debug(f"Content of {cert_file}: \n{cert_content}")
    except Exception as e:
        logger.error(f"Error reading {cert_file}: {e}")


# Print contents of the certificate files
print_cert_content(AWS_CA_CERT)
print_cert_content(AWS_CERT)
print_cert_content(AWS_PRIVATE_KEY)


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
