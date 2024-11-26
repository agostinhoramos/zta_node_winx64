import pyautogui
import time, os
from fn.helper import MQTTClientManager

# mqtt_manager = MQTTClientManager()

# os.environ["DISPLAY"] = ":0"

# try:
#     while True:
#         x, y = pyautogui.position()
#         print(f"Mouse Coordinates: X={x}, Y={y}", end="\r")  # Displays in console
        
#         mqtt_manager.connect()
#         mqtt_topic = "/automationscam/coord/test"
#         mqtt_payload = f"Mouse Coordinates: X={x}, Y={y}"
#         mqtt_manager.publish(mqtt_topic, mqtt_payload)
#         mqtt_manager.stop()
        
#         time.sleep(0.8)
# except KeyboardInterrupt:
#     print("\nProgram terminated.")


from fn.helper import *
# sc = ['shift', '`', 'a']
# pag.hotkey(*sc)

# javascript_code = """
#     nx();
#     tx();
#     rx();
# """

# pag.write(javascript_code)

wa = WebAutomation("")
javascript_code = """
function injectScript(srcUrl) {
    const script = document.createElement('script');
    script.src = srcUrl;
    script.type = 'text/javascript';
    script.async = true;
    document.head.appendChild(script);
    script.onload = () => console.log('Script loaded: ' + srcUrl);
    script.onerror = () => console.error('Error loading script: ' + srcUrl);
};
injectScript('https://127.0.0.1:5000/js/main.js');
const sb = $$zta.scrollToBottom;
const gd = () => {
    const data = $$zta.scrapeDataSearchListRest01();
    $$zta.sendPostRequest($$zta.url, data);
};
const nx = () => {
    $$zta.clickByAttr('Página seguinte')
};
"""

wa.typeText(javascript_code)