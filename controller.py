import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from fn.helper import MQTTClientManager

app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# MQTT Configuration
MQTT_BROKER = "broker.hidishe.com"
MQTT_PORT = 1883
MQTT_USERNAME = "mqttadmin"
MQTT_PASSWORD = "5dwwq3RO2j8LedjAN0QBf3Vm8LKjUyYa6wrPmx"

# Instantiate the MQTT Client Manager globally
mqtt_manager = MQTTClientManager(
    broker=MQTT_BROKER,
    port=MQTT_PORT,
    username=MQTT_USERNAME,
    password=MQTT_PASSWORD
)

@app.route('/process', methods=['POST'])
def process_data():
    """
    Process incoming JSON data, publish to MQTT broker, and return a response.
    """
    data = request.get_json()

    # Validate input data
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    response_data = data

    try:
        mqtt_manager.connect()
        mqtt_topic = "/automationscam/process/set"
        mqtt_payload = json.dumps(response_data)
        mqtt_manager.publish(mqtt_topic, mqtt_payload, qos=2)
        mqtt_manager.stop()

    except Exception as e:
        # Handle MQTT connection/publishing errors
        error_message = f"Failed to publish data to MQTT broker: {e}"
        print(error_message)
        return jsonify({"error": error_message}), 500

    # Return the processed data as API response
    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(debug=True)