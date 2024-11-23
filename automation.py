import pyautogui as pag
import random,re
from pathlib import Path
from scripts.tripadvisor_pt import task001

class Automation:
    """Main class for automating web actions."""
    def __init__(self):
        ...

    def perform_actions(self):
        """Executes web automation actions."""
        

    def run(self):
        """Sets up folders, executes actions, and checks downloads."""
        self.perform_actions()
        
        user_actions = task001.UserTask()
        user_actions.execute_custom_actions()

auto = Automation()