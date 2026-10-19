# Launcher Script
# used to emulate the power circuit in it's absense in order to run the main script

import subprocess as sp
import board, digitalio
import time

motion = digitalio.DigitalInOut(board.D25) # type: ignore
# use push button
motion.direction = digitalio.Direction.INPUT

while True:
    if motion.value:
        print("button!")
        time.sleep(5)
        #sp.run(["python3", "main.py"])
    else:
        time.sleep(0.1)