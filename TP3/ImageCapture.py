import subprocess
try:
    import pyscreenshot
except ImportError as err:
    subprocess.check_call(['pip', 'install', 'pyscreenshot'])
    import pyscreenshot

import uuid
from pathlib import Path
import pygame

class ImageCapture():
    def __init__(self, screen_spawn_position):
        # Parameters to adjust the window to capture
        self.count = 0
        self.window_left = screen_spawn_position[0]
        self.window_top = screen_spawn_position[1]

        # Prepare the directories in which the images are stored
        Path("./images/").mkdir(parents=True, exist_ok=True)
        Path("./images/up/").mkdir(parents=True, exist_ok=True)
        Path("./images/down/").mkdir(parents=True, exist_ok=True)
        Path("./images/right/").mkdir(parents=True, exist_ok=True)
        Path("./images/live/").mkdir(parents=True, exist_ok=True)
        self.ss_id = uuid.uuid4()

    def take_screenshot(self, key):
        # Save the screenshot
        self.count += 1
        screenshot = pyscreenshot.grab(bbox=(self.window_left+200, self.window_top + 190, self.window_left + 475, self.window_top + 500))
        screenshot.save("./images/{}/{}.png".format(key, self.count))

    def capture(self, userInput):
        # Take a screenshot on command and tag it on the pressed button folder
        if userInput[pygame.K_UP]:
            self.take_screenshot("up")

        elif userInput[pygame.K_DOWN]:
            self.take_screenshot("down")

        else:
            self.take_screenshot("right")

    def capture_live(self):
        # Automatically take a screenshot for the Tensorflow model to work
        screenshot = pyscreenshot.grab(bbox=(self.window_left+200, self.window_top + 190, self.window_left + 475, self.window_top + 500))

        #screenshot = pyscreenshot.grab(bbox=(self.window_left+200, self.window_top + 190, self.window_left + 425, self.window_top + 500))
        #screenshot = pyscreenshot.grab(bbox=(self.window_left+240, self.window_top + 190, self.window_left + 425, self.window_top + 510))
        #screenshot = pyscreenshot.grab(bbox=(self.window_left+240, self.window_top + 190, self.window_left + 425, self.window_top + 510))
        #screenshot = pyscreenshot.grab(bbox=(self.window_left+140, self.window_top + 140, self.window_left + 465, self.window_top + 540))
        #screenshot = pyscreenshot.grab(bbox=(self.window_left+50, self.window_top + 140, self.window_left + 965, self.window_top + 640))
        
        screenshot.save("./images/live/temp.png")