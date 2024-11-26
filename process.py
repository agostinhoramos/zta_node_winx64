import os, time
from celery import Celery

from fn.helper import *
import pyautogui

from worker.browser import Chrome

app = Celery(
    'myapp',
    broker='pyamqp://rabbit:G82cAy4o@127.0.0.1//'
)

chromeTask = Chrome()

@app.task
def chromeTaskRun():    
    os.environ["DISPLAY"] = ":0"
    chromeTask.stop()
    
@app.task
def fakeUserMouseMove(move_count=10, delay=0.5):
    time.sleep(2)
    screen_width, screen_height = pyautogui.size()

    for _ in range(move_count):
        random_x = random.randint(0, screen_width - 1)
        random_y = random.randint(0, screen_height - 1)
        
        MouseHandler.move_and_click(random_x, random_y)

        time.sleep(delay)