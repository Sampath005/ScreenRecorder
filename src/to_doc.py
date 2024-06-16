import datetime
from PIL import ImageGrab
import numpy as np
import cv2
from pynput.mouse import Listener
from docx import Document
from docx.shared import Inches
import signal
import sys
import os

# Initialize document
doc = Document()
screenshot_counter = 0
screenshot_files = []


def on_click(x, y, button, pressed):
    global screenshot_counter
    if pressed and button.name == 'left':
        # Capture screenshot
        img = ImageGrab.grab()
        img_np = np.array(img)
        img_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

        # Save screenshot as image file
        time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        screenshot_file = f'{time_stamp}.png'
        cv2.imwrite(screenshot_file, img_final)
        screenshot_files.append(screenshot_file)

        # Add screenshot to Word document
        doc.add_picture(screenshot_file, width=Inches(6))
        screenshot_counter += 1

        print(f'Screenshot {screenshot_counter} captured and added to document.')


# Set up mouse listener
listener = Listener(on_click=on_click)
listener.start()


def signal_handler(sig, frame):
    print('You pressed Ctrl+C! Saving document...')
    # Save the document
    doc.save('screenshots.docx')
    print('Document saved as screenshots.docx')

    # Delete the image files
    for file in screenshot_files:
        if os.path.exists(file):
            os.remove(file)
            print(f'Deleted {file}')

    listener.stop()
    sys.exit(0)


# Set up signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

print("Press 'Ctrl+C' to stop the program and save the document.")

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    signal_handler(None, None)
