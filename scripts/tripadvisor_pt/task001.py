from fn.helper import *
class UserTask:
    """Class for user-defined custom actions."""
    def __init__(self):
        ROOT_FOLDER = "C:/Users/webmaster/Documents/project/webscam/tmp"
        self.wa = WebAutomation(ROOT_FOLDER)
        self.mqtt = MQTTClientManager()

    def execute_custom_actions(self):
               
        def on_message(client, userdata, msg):
            """Callback triggered when a message is received."""
            try:
                payload = msg.payload.decode("utf-8")
                data = json.loads(payload)
                print(f"Received message on '{msg.topic}': {data}")
                
                MouseHandler.move_and_click(200, 780, click=True)
                MouseHandler.move_and_click(219, 48, click=True)
                
                # pag.write('https://www.tripadvisor.pt/Restaurant_Review-g4914446-d25035356-Reviews-El_Pimenton-Amora_Setubal_District_Alentejo.html')
                # pag.press('enter')
                # time.sleep(3)
                # MouseHandler.move_and_click(471, 149)
                # pag.press('end')
                # time.sleep(2)
                
                pag.hotkey('ctrl', 'shift', 'i')
                time.sleep(1)
                pag.hotkey('ctrl', 'l')

                javascript_code = "$$zta.load()"
                pag.typewrite(javascript_code.splitlines(), interval=0.01)
                time.sleep(600)
                pag.hotkey('alt', 'f4')
                
            except json.JSONDecodeError:
                print(f"Received non-JSON message on '{msg.topic}': {msg.payload}")
            except Exception as e:
                print(f"Error processing message: {e}")
            
        self.mqtt.client.on_message = on_message
        self.mqtt.connect()
        self.mqtt.subscribe("/automationscam/process/t/#")
        
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("Exiting...")
            self.mqtt.stop()