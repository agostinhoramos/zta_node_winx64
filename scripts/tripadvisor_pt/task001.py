from fn.helper import *

class UserTask:
    """Class for user-defined custom actions."""
    def __init__(self):
        ROOT_FOLDER = "C:/Users/webmaster/Documents/project/webscam/tmp"
        self.wa = WebAutomation(ROOT_FOLDER)

    def execute_custom_actions(self):
        """
        Executes user-defined custom actions.
        """
        MouseHandler.move_and_click(200, 780, click=True)
        MouseHandler.move_and_click(219, 48, click=True)
        pag.write('https://www.tripadvisor.pt/Restaurant_Review-g4914446-d25035356-Reviews-El_Pimenton-Amora_Setubal_District_Alentejo.html')
        pag.press('enter')
        time.sleep(3)
        MouseHandler.move_and_click(471, 149)
        pag.press('end')
        time.sleep(2)
        pag.hotkey('ctrl', 'shift', 'i')
        time.sleep(3)
        pag.hotkey('ctrl', 'l')

        javascript_code = """
        $$at.openDetails()
        """
        self.wa.execute_javascript_code(javascript_code.splitlines())
        time.sleep(1)
        pid = "001"
        javascript_code = """
const sd = $$at.scrapeData(selectors);
const p = {source: location.href, pid: '"""+pid+"""', data: sd};
$$at.sendPostRequest($$at.url, p).then(response => { }) .catch(error => { });
"""
        self.wa.execute_javascript_code(javascript_code.splitlines())
        time.sleep(1)
        pag.hotkey('alt', 'f4')