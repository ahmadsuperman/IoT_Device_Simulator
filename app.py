# Import necessary libraries and modules
from sensor import SensorSimulator
from iothub import IotHub
from config import Config
import paho.mqtt.client as mqtt
import time
import sys
import ssl
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve the connection string from the environment variables
connection_string = os.getenv('CONNECTION_STRING')

# Check if the connection string is available, if not, exit the program
if connection_string == '':
    print("Missing Connection String")
    sys.exit(1)

# Create configuration, IoT hub, and sensor objects
config = Config(connection_string)
iot = IotHub(config.hub_address, config.device_id, config.shared_access_key)
sensor = SensorSimulator()

# Define the rate at which the sensor data is sampled and sent
sample_rate_in_seconds = 5

# Define callback functions for different MQTT client events

# Callback when the client connects to the server


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: %s" % rc)
    client.subscribe(iot.hub_topic_subscribe)

# Callback when the client disconnects from the server


def on_disconnect(client, userdata, rc):
    print("Disconnected with result code: %s" % rc)
    # Reconfigure the username and password on disconnect (useful for reconnection)
    client.username_pw_set(iot.hub_user, iot.generate_sas_token(
        iot.endpoint, iot.shared_access_key))

# Callback when a PUBLISH message is received from the server


def on_message(client, userdata, msg):
    print("Message received: %s" % msg)

# Callback when the client has successfully sent a message


def on_publish(client, userdata, mid):
    print("Message {0} sent from {1} at {2}".format(
        str(mid), config.device_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

# Function to publish sensor data to the IoT hub indefinitely


def publish():
    while True:
        try:
            # Read data from the sensor
            reading = sensor.read()
            # Convert the sensor data to JSON format
            msg = json.dumps(reading)
            print(msg)
            # Publish the sensor data to the IoT hub
            client.publish(iot.hub_topic_publish, msg)
            # Wait for the defined sample rate interval
            time.sleep(sample_rate_in_seconds)
        except KeyboardInterrupt:
            # Handle script interruption (e.g., by pressing Ctrl+C)
            print("IoTHubClient sample stopped")
            return
        except:
            # Handle any other exception and wait 4 seconds before continuing
            print("Unexpected error")
            time.sleep(4)


# Create an MQTT client instance with the device ID and MQTT protocol version
client = mqtt.Client(config.device_id, mqtt.MQTTv311)

# Set up event callbacks for the client
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_publish = on_publish

# Set the username and password for MQTT client from the IoT hub credentials
client.username_pw_set(iot.hub_user, iot.generate_sas_token())

# Configure the MQTT client to use SSL/TLS
client.tls_set()

# Connect the MQTT client to the IoT hub using the hub address and the default MQTT port over SSL/TLS
client.connect(config.hub_address, 8883)

# Start a thread in the background to handle network events, including reconnection
client.loop_start()

# Begin publishing sensor data to the IoT hub
publish()
