import time
import os
import asyncio
from conf import debug

while True:
    if debug:
        n = 0
    else:
        n = 5
    os.system("python3 C:\\Users\\qvalador\\Documents\\Code\\scout\\bot.py")
    print("the bot died, restarting in 5")
    time.sleep(n)