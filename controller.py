import os, json
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from flask_talisman import Talisman
from fn.helper import MQTTClientManager

app = Flask(__name__)

Talisman(app, content_security_policy=None)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

mqtt_manager = MQTTClientManager()

def process_data():
    """
    Process incoming JSON data, publish to MQTT broker, and return a response.
    """
    
    try:
        
        data = request.get_json(force=True)

        # Validate input data
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        decoded_data = json.loads(json.dumps(data), strict=False)
        
        mqtt_manager.connect()
        
        mqtt_topic = "/automationscam/process/set"
        mqtt_payload = decoded_data
        mqtt_manager.publish(mqtt_topic, mqtt_payload)
        mqtt_manager.stop()
    
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Invalid JSON data: {str(e)}"}), 400

    except Exception as e:
        error_message = f"Failed to process request: {str(e)}"
        print(error_message)
        return jsonify({"error": error_message}), 500

    return jsonify(decoded_data), 200

app.add_url_rule(
    "/process",
    view_func=process_data,
    methods=['POST']
)

def remote_js():
    file_path = "scripts/tripadvisor_pt/injectedJS.js"
    
    js_content = ""
    with open(file_path, "r", encoding="utf-8") as file:
        js_content = file.read()
    # Criar uma resposta com o tipo de conteúdo apropriado
    response = Response(js_content, mimetype='application/javascript')
    response.headers['Cache-Control'] = 'public, max-age=3600'  # Cache por 1 hora
    return response

app.add_url_rule(
    "/js/main.js",
    view_func=remote_js,
    methods=['GET']
)