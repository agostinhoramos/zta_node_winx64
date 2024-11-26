from fn.helper import *

from process import chromeTask, chromeTaskRun, fakeUserMouseMove

def inject_javascript(typeText):
    time.sleep(2)
    javascript_code = "const i=(e)=>{const t=document.createElement('script');t.src=e,t.type='text/javascript',t.async=!0,document.head.appendChild(t),t.onload=()=>$$zta.OK(),t.onerror=()=>$$zta.NOK()};i('https://127.0.0.1:5000/m');"
    typeText(javascript_code, delay=180)
    pag.hotkey('enter')
    time.sleep(2)

def openTerminal():
    time.sleep(3)
    #MouseHandler.move_and_click(28, 774, click=True)
    pag.hotkey('ctrl', 'shift', 'i')
    time.sleep(1)
    pag.hotkey('ctrl', 'l')
    time.sleep(2)
    
def addSnippets(typeText):
    javascript_code = """
const sb = $$zta.scrollToBottom;
const gd = () => {
    const data = $$zta.scrapeDataSearchListRest01();
    $$zta.sendPostRequest($$zta.url, data);
};
const nx = () => {
    $$zta.clickByAttr('Página seguinte')
};
"""
    typeText(javascript_code, delay=120)
    pag.hotkey('enter')
    
    
def openBrowserPage(typeText, url, reopen = False):
    if reopen:
        chromeTask.start(url)
    else:
        javascript_code=f"""
document.location='{url}'
"""
        typeText(javascript_code, delay=120)
        pag.hotkey('enter')
        time.sleep(5)
        
                            
class UserTask:
    """Class for user-defined custom actions."""
    def __init__(self):
        ROOT_FOLDER = "C:/Users/webmaster/Documents/project/webscam/tmp"
        self.wa = WebAutomation(ROOT_FOLDER)
        self.mqtt = MQTTClientManager()

    def execute_custom_actions(self):
        
        chromeTaskRun.delay()
               
        def on_message(client, userdata, msg):
            """Callback triggered when a message is received."""
            try:
                payload = msg.payload.decode("utf-8")
                data = json.loads(payload)
                print(f"Received message on '{msg.topic}': {data}")
                
                if msg.topic == "/automationscam/process/t/0001":
                    
                    # data["target_url"]
                    # data["num_task"]
                    
                    urls = [
                        'https://www.tripadvisor.pt/Search?q=P%C3%A3o&geo=1&ssrc=e&searchNearby=false&searchSessionId=000d8c84a7fb03fc.ssid&offset=0',
                        'https://www.tripadvisor.pt/Search?q=Peixe&geo=1&ssrc=e&searchNearby=false&searchSessionId=000d8c84a7fb03fc.ssid&offset=0'
                        'https://www.tripadvisor.pt/Search?q=Comida&geo=1&ssrc=e&searchNearby=false&searchSessionId=000d8c84a7fb03fc.ssid&offset=0'
                        'https://www.tripadvisor.pt/Search?q=Delicia&geo=1&ssrc=e&searchNearby=false&searchSessionId=000d8c84a7fb03fc.ssid&offset=0'
                    ]
                    
                    reopen = True
                    for _url in urls:
                        openBrowserPage(self.wa.typeText, _url, reopen)
                        if reopen:
                            openTerminal()
                            time.sleep(5)
                            
                        inject_javascript(self.wa.typeText)
                        addSnippets(self.wa.typeText)
                        
                        for _ in range(0, 34):
                            javascript_code = "sb();"
                            self.wa.typeText(javascript_code)
                            pag.hotkey('enter')
                            time.sleep(1)
                            javascript_code = "gd();"
                            self.wa.typeText(javascript_code)
                            pag.hotkey('enter')
                            time.sleep(1)
                            javascript_code = "nx();"
                            self.wa.typeText(javascript_code)
                            pag.hotkey('enter')
                            time.sleep(1)
                            
                            fakeUserMouseMove.delay(move_count=3, delay=0.3)
                        
                        reopen = False                
                    
                    time.sleep(3)
                
                if msg.topic == "/automationscam/process/t/0002":           
                    javascript_code = """
                    $$zta.load()
                    """
                    self.wa.execute_javascript_code(javascript_code.splitlines())
                    time.sleep(1)
                    javascript_code = """
                    const cj = JSON.parse($$zta.conf);
                    const sd = $$zta.scrapeData(cj.selectors);
                    $$zta.sendPostRequest($$zta.url, sd)
                    """
                    self.wa.execute_javascript_code(javascript_code.splitlines())
                    time.sleep(1)
                    pag.hotkey('enter')
                    
                time.sleep(1)
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