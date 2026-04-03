import traceback
import sys
sys.path.insert(0, r'k:\BURGER\burger-bot')
from command_handler import CommandHandler
try:
    h = CommandHandler()
    h.process('tell me a joke')
except Exception as e:
    pass # CommandHandler catches it internally. Wait.
