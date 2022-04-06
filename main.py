#!/usr/bin/env python3
from PIL import Image
import urllib.request
import os
import json


URL_IMAGE = r"https://raw.githubusercontent.com/CorentinGC/reddit-place-kcorp/" \
            r"5ccd64740f9dfd842081c635c3c05c366283e025/overlay.png"
LOCAL_NAME = os.path.join(os.path.dirname(__file__), os.path.basename(URL_IMAGE))
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

USERNAME = ""
PASSWORD = ""

# Ratio between r/place and our French overlay
RATIO = 3

# We focus on Zidane, because we love him and spanish peoples don't apparently ..
LEFT, UPPER = 85, 1520
RIGHT, LOWER = 165, 1620


if __name__ == '__main__':
    # Retrieve image
    with urllib.request.urlopen(URL_IMAGE) as tmp:
        with open(LOCAL_NAME, "wb") as i:
            i.write(tmp.read())
    im = Image.open(LOCAL_NAME)

    # Crop image on interesting part
    # French overlay has a size of 6000 * 6000 and r/place has a size of 2000 * 2000
    # This is why we need to multiply by RATIO in order to get the interesting part of the image
    cropped_im = im.crop((LEFT * RATIO, UPPER * RATIO, RIGHT * RATIO, LOWER * RATIO))

    # Resize cropped image in order to fit the place size
    r_im = cropped_im.resize((RIGHT - LEFT, LOWER - UPPER))
    # r_im.show()

    # Generate the config
    tmp_cfg = {
        "image_path": LOCAL_NAME,
        "image_start_coords": [LEFT, UPPER],
        "thread_delay": 2,
        "workers": {
            USERNAME: {
                "password": PASSWORD,
                "start_coords": [0, 0]
            }
        }
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(tmp_cfg, f)
