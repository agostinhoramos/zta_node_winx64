# import pyautogui
# import time
# from fn.helper import MQTTClientManager

# mqtt_manager = MQTTClientManager()

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


import pyautogui as pag

sc = ['shift', '`', 'a']
pag.hotkey(*sc)