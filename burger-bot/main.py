import sys
import os
import threading
import logging
import time

# Ensure imports work from current dir
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from character_ui import BurgerUI
from voice_engine import VoiceEngine
from command_handler import CommandHandler
from admin_panel import AdminPanel
import automation

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

class BurgerApp:
    def __init__(self):
        self.cmd_handler = CommandHandler()
        self.settings_window = None
        
        # Initialize Voice engine
        self.voice_engine = VoiceEngine(
            state_callback=self.on_state_change,
            process_command_callback=self.on_command_received
        )
        
        # Initialize UI (needs to run on main thread)
        self.ui = BurgerUI(
            start_voice_engine=self.start_systems,
            command_handler_fn=self.on_command_received,
            open_settings_fn=self.toggle_settings
        )

    def toggle_settings(self):
        """Launch or focus personal customization panel."""
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = AdminPanel(self.ui)
        else:
            self.settings_window.focus()

    def on_state_change(self, state, text):
        """Called by voice engine to push updates to the UI."""
        self.ui.update_state(state, text)

    def on_command_received(self, command_text):
        """Called by voice engine when user says a command."""
        logger.info(f"Received command: {command_text}")
        
        # We process the command using Cohere API in a background thread to avoid blocking UI
        def _process():
            intent = self.cmd_handler.process(command_text)
            logger.info(f"Intent extracted: {intent}")
            action = intent.get("action", "chat")
            param = intent.get("param", "")
            response = intent.get("response", "I'm not sure what you mean.")
            
            # Perform Action
            if action == "open_app":
                success = automation.open_anything(param)
                if not success:
                    response = f"I couldn't find how to open {param}."
            
            elif action == "play_music":
                automation.play_music(param)
                
            elif action == "search_web":
                automation.search_web(param)
                
            elif action == "set_volume":
                automation.set_volume(param)
                
            elif action == "set_brightness":
                automation.set_brightness(param)
                
            elif action == "system_action":
                status = automation.perform_system_action(param)
                response = f"{response}. {status}"
                
            elif action == "chat":
                pass # Just chat, response handles it
                
            # Speak Response
            self.voice_engine.speak(response)
            
        threading.Thread(target=_process, daemon=True).start()

    def start_systems(self):
        """Called automatically after UI launches to start the background voice systems."""
        logger.info("Initializing BURGER systems...")
        self.voice_engine.speak("Hii boss, what's up? What can I do for you?")
        self.voice_engine.start()

    def run(self):
        # Run Tkinter mainloop
        self.ui.mainloop()

if __name__ == "__main__":
    print("🍔 Starting BURGER AI Character...")
    app = BurgerApp()
    app.run()
