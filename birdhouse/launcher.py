# Launcher Script
# used to emulate the power circuit in it's absense in order to run the main script

import subprocess as sp
import board, digitalio
import sys
import time

motion = digitalio.DigitalInOut(board.D25) # type: ignore
# use push button
motion.direction = digitalio.Direction.INPUT

while True:
    try:
        if motion.value:
            print("Button pressed! Starting...")
            sp.run([sys.executable, "main.py"])
            time.sleep(5)
            print("off cooldown")
        else:
            time.sleep(0.1)
    except KeyboardInterrupt:
        break
print("Goodbye!")