#!/usr/bin/env python
import subprocess
import sys
import os

# Change to bot_1 directory and run bot_1.py
os.chdir(os.path.join(os.path.dirname(__file__), 'bot_1'))
subprocess.run([sys.executable, 'bot_1.py'])
