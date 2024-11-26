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
    
def smooth_move(x1, y1, x2, y2, duration):
    steps = int(duration * 100)
    for i in range(steps):
        
        t = i / float(steps)
        
        xt = int((1 - t) * x1 + t * x2 + random.randint(-3, 3))
        yt = int((1 - t) * y1 + t * y2 + random.randint(-3, 3))
        pyautogui.moveTo(xt, yt, duration=0.01)

@app.task
def fakeUserMouseMove(move_count=10, min_delay=0.3, max_delay=5.0):
    time.sleep(2)
    pyautogui.FAILSAFE = False
    screen_width, screen_height = pyautogui.size()

    for _ in range(move_count):
        random_x = random.randint(0, screen_width - 1)
        random_y = random.randint(0, screen_height - 1)

        current_x, current_y = pyautogui.position()

        duration = random.uniform(1, 2)
        smooth_move(current_x, current_y, random_x, random_y, duration)

        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)