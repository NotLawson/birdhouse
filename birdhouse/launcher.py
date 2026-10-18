# Launcher Script
# used to emulate the power circuit in it's absense in order to run the main script

import subprocess as sp
import board, digitalio

sp.run(["python3", "main.py"])