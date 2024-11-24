import pyautogui as pag
import random
import time
import subprocess
import hashlib
import os, re, json
import shutil
from pathlib import Path
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

class MouseHandler:
    """Handles mouse actions."""
    @staticmethod
    def move_and_click(x, y, click=False):
        """
        Moves the mouse to specific coordinates and optionally clicks.

        :param x: X-coordinate.
        :param y: Y-coordinate.
        :param click: Whether to click at the position.
        """
        pag.moveTo(x, y, duration=random.uniform(1, 2))
        if click:
            pag.click()
        time.sleep(0.1)

class DownloadManager:
    """Manages downloads and waits for their completion."""
    @staticmethod
    def wait_for_download(folder_path, filename_prefix, timeout=60):
        """
        Waits for a download to finish by checking for specific files.

        :param folder_path: Path to the folder where downloads are saved.
        :param filename_prefix: Prefix of the file name.
        :param timeout: Maximum time to wait (in seconds).
        :return: True if the download completes, False if it times out.
        """
        start_time = time.time()
        folder = Path(folder_path)

        while time.time() - start_time < timeout:
            files_in_folder = list(folder.glob(f"{filename_prefix}*"))
            downloading_files = [file for file in files_in_folder if file.suffix in ('.crdownload', '.part', '.tmp')]

            if files_in_folder and not downloading_files:
                print(f"Download completed: '{files_in_folder[0]}'")
                return True

            time.sleep(1)

        print("Timeout reached. The download may not have completed.")
        return False

class Utils:
    """Utility functions."""
    @staticmethod
    def string_to_sha256(input_string):
        """Converts a string to its SHA-256 hash."""
        return hashlib.sha256(input_string.encode('utf-8')).hexdigest()

    @staticmethod
    def execute_command(command):
        """Executes a shell command."""
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            
    @staticmethod
    def delete_folder(folder_path):
        """Deletes a folder and all its contents, ensuring everything is removed."""
        if not os.path.exists(folder_path):
            print(f"The folder '{folder_path}' does not exist.")
            return

        try:
            shutil.rmtree(folder_path, ignore_errors=False)
            print(f"Folder '{folder_path}' and all its contents have been deleted successfully.")
        except Exception as e:
            print(f"Error occurred while deleting folder '{folder_path}': {e}")
            # Retry file-by-file deletion
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                    except Exception as file_error:
                        print(f"Failed to delete file: {file_error}")
                for dir in dirs:
                    try:
                        os.rmdir(os.path.join(root, dir))
                    except Exception as dir_error:
                        print(f"Failed to delete folder: {dir_error}")

            # Final attempt to delete the root folder
            try:
                os.rmdir(folder_path)
            except Exception as final_error:
                print(f"Failed to delete the root folder '{folder_path}': {final_error}")
                
class WebAutomation:
    """Main class for automating web actions."""
    def __init__(self, root_folder):
        self.root_folder = Path(root_folder)
        self.temp_folder = None
        self.file_full_path = None
        self.hash_file = None
        
    def minify_js(self, javascript_code):
        """
        Minifies the provided JavaScript code by removing spaces, newlines, and unnecessary indentation.
        
        :param javascript_code: The JavaScript code to minify.
        :return: The minified JavaScript code.
        """
        # Ensure the input is a string (in case it's passed as a list of characters)
        if isinstance(javascript_code, list):
            javascript_code = ''.join(javascript_code)  # Join list into a single string

        # Remove all unnecessary spaces and newlines
        minified_code = re.sub(r'\s+', ' ', javascript_code)  # Replaces multiple spaces with a single space
        minified_code = re.sub(r'\n+', '', minified_code)  # Removes all newlines
        return minified_code.strip()

    def setup_temp_folder(self):
        """Sets up the temporary folder and file name."""
        hash_folder = random.getrandbits(128)
        self.temp_folder = self.root_folder / Utils.string_to_sha256(str(hash_folder))
        self.temp_folder.mkdir(parents=True, exist_ok=True)
        self.hash_file = random.getrandbits(16)
        self.file_full_path = self.temp_folder / f"{self.hash_file}_file.html"

    def execute_javascript_code(self, code):
        """Executes the provided JavaScript code in the browser console."""
        minified_code = self.minify_js(code)
        for line in minified_code:
            for char in line:
                self.type_special_characters(char)
                
        pag.press("enter")

    def type_special_characters(self, char):
        """Types characters considering special keys (like '{', '}', etc.)."""
        
        special_keys = {
            'à': ['shift', '`', 'a'],  # Grave accent + 'a'
            'á': ['shift', '´', 'a'],  # Acute accent + 'a'
            'ã': ['~', 'a'],           # Tilde + 'a'
            'è': ['shift', '`', 'e'],  # Grave accent + 'e'
            'é': ['´', 'e'],           # Acute accent + 'e'
            'ê': ['shift', '^', 'e'],  # Circumflex + 'e'
            'í': ['shift', '´', 'i'],  # Acute accent + 'i'
            'ó': ['shift', '´', 'o'],  # Acute accent + 'o'
            'ô': ['shift', '^', 'o'],  # Circumflex + 'o'
            'ú': ['shift', '´', 'u'],  # Acute accent + 'u'
            'ç': ['altgr', 'c'],       # 'ç' with AltGr
            'Ç': ['altgr', 'shift', 'c'],  # 'Ç' with AltGr + Shift
            'À': ['shift', '`', 'A'],  # Grave accent + 'A'
            'Á': ['shift', '´', 'A'],  # Acute accent + 'A'
            'É': ['´', 'E'],           # Acute accent + 'E'
            'Ê': ['shift', '^', 'E'],  # Circumflex + 'E'
            'Ô': ['shift', '^', 'O'],  # Circumflex + 'O'
            'Ú': ['shift', '´', 'U'],  # Acute accent + 'U'
        
            '{': ['alt', 'ctrl', '7'],
            '}': ['alt', 'ctrl', '0'],
            '[': ['alt', 'ctrl', '8'],
            ']': ['alt', 'ctrl', '9'],
            "'": ["'"],
            '"': ['shift', '2']
        }

        if char in special_keys:
            pag.hotkey(*special_keys[char])
        else:
            try:
                pag.typewrite(char, interval=0.01)
            except Exception as e:
                print(f"Error typing character {char}: {e}")

class MQTTClientManager:
    """Handles MQTT operations: connect, publish, and subscribe."""

    def __init__(self):
        self.broker = os.getenv("MQTT_BROKER")
        self.port = int(os.getenv("MQTT_PORT"))
        self.username = os.getenv("MQTT_USER")
        self.password = os.getenv("MQTT_PASS")
        self.keepalive = int(os.getenv("MQTT_KEEPALIVE"))
        self.client = mqtt.Client()
        self.subscriptions = []  # Track subscribed topics to avoid duplication

        # Set username and password for the broker
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)

        # Attach default callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        """Callback triggered when the client connects to the broker."""
        if rc == 0:
            print("Successfully connected to the MQTT broker.")
            for topic in self.subscriptions:
                self.client.subscribe(topic)
        else:
            print(f"Failed to connect to MQTT broker. Return code: {rc}")

    def _on_message(self, client, userdata, msg):
        """Callback triggered when a message is received."""
        try:
            payload = msg.payload.decode("utf-8")
            data = json.loads(payload)
            print(f"Received message on '{msg.topic}': {data}")
        except json.JSONDecodeError:
            print(f"Received non-JSON message on '{msg.topic}': {msg.payload}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def connect(self):
        """Connects to the MQTT broker."""
        try:
            self.client.connect(self.broker, self.port, self.keepalive)
            self.client.loop_start()  # Start the network loop in a background thread
            print("MQTT client loop started.")
        except Exception as e:
            print(f"Error connecting to MQTT broker: {e}")

    def publish(self, topic, message):
        """Publishes a message to a specified topic."""
        try:
            result = self.client.publish(topic, json.dumps(message))
            status = result[0]
            if status == 0:
                print(f"Message published to '{topic}': {message}")
            else:
                print(f"Failed to publish message to '{topic}'.")
        except Exception as e:
            print(f"Error publishing message: {e}")

    def subscribe(self, topic):
        """
        Subscribes to a specific topic.
        Avoids duplicate subscriptions by checking the internal list.
        """
        if topic not in self.subscriptions:
            try:
                self.client.subscribe(topic)
                self.subscriptions.append(topic)
                print(f"Subscribed to '{topic}'.")
            except Exception as e:
                print(f"Error subscribing to '{topic}': {e}")
        else:
            print(f"Already subscribed to '{topic}'.")

    def stop(self):
        """Stops the MQTT client loop and disconnects from the broker."""
        try:
            self.client.loop_stop()
            self.client.disconnect()
            print("MQTT client disconnected.")
        except Exception as e:
            print(f"Error stopping MQTT client: {e}")