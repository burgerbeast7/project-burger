import sys
import os
sys.path.insert(0, r"k:\BURGER\burger-bot")
from command_handler import CommandHandler
import logging
logging.basicConfig(level=logging.DEBUG)

handler = CommandHandler()
res = handler.process("Hello, testing")
print("RESULT:", res)
