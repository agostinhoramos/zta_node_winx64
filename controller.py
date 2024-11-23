import os, json
from flask import Flask, request, jsonify
from flask_cors import CORS
from fn.helper import MQTTClientManager

app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

mqtt_manager = MQTTClientManager()

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
        mqtt_manager.publish(mqtt_topic, mqtt_payload)
        mqtt_manager.stop()

    except Exception as e:
        # Handle MQTT connection/publishing errors
        error_message = f"Failed to publish data to MQTT broker: {e}"
        print(error_message)
        return jsonify({"error": error_message}), 500

    # Return the processed data as API response
    return jsonify(response_data), 200

app.add_url_rule(
    "/process",
    view_func=process_data,
    methods=['POST']
)

def remote_js():
    return "example JS script", 200

app.add_url_rule(
    "/js/main.js",
    view_func=remote_js,
    methods=['GET']
)