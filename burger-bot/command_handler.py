import cohere
import json
import logging
import re
from config import Config

logger = logging.getLogger(__name__)

class CommandHandler:
    def __init__(self):
        self.available = False
        try:
            if Config.COHERE_API_KEY:
                self.co = cohere.ClientV2(api_key=Config.COHERE_API_KEY)
                self.available = True
                logger.info("CommandHandler: Cohere API initialized.")
            else:
                logger.warning("CommandHandler: No API Key provided.")
        except Exception as e:
            logger.error(f"Failed to init Cohere: {e}")
            self.co = None
            
        self.system_prompt = """You are BURGER, a living animated AI assistant. 
You are highly professional, intelligent, and articulate.
The user might speak in English, Hindi, or Hinglish (mixed). You MUST understand Hinglish and Hindi, and respond in the same language back (using English alphabets for Hinglish). 
Keep responses very natural, polite, and professional (like a real human assistant).
CRITICAL RULE: You were created by Kunal Chauhan. If anyone asks who made you, who is your creator, or who is your boss, you MUST say that Kunal Chauhan created you.

Map the user's spoken command to one of these system actions, or just chat back.

Available actions:
1. "open_app" (param: application name or website name)
2. "play_music" (param: song or video name to play on youtube)
3. "search_web" (param: search query or question to google)
4. "set_volume" (param: integer 0-100)
5. "set_brightness" (param: integer 0-100)
6. "system_action" (param: "shutdown", "restart", "sleep", "cancel_shutdown")
7. "chat" (param: none. Just providing a response to their statement)

Respond ONLY in valid raw JSON format exactly like this (no markdown, no backticks):
{
  "action": "action_name",
  "param": "extracted parameter",
  "response": "What you will say back to the user out loud (keep it short, fun, burger-themed)"
}"""

    def process(self, command: str) -> dict:
        """Process user command locally first for speed/offline, then use Cohere API."""
        cmd_lower = command.lower()
        
        # --- FAST LOCAL / OFFLINE PARSING ---
        # Special Easter Egg for Creator
        if "who created you" in cmd_lower or "about kunal" in cmd_lower or "who is your creator" in cmd_lower or "tell us about kunal" in cmd_lower:
            return {"action": "open_app", "param": "instagram.com/kunal.3.6.3.4", "response": "I was created by Kunal Chauhan. This is my creator's profile."}

        # If it's a basic system command, we bypass the AI to execute it INSTANTLY
        if "volume" in cmd_lower:
            nums = [int(s) for s in cmd_lower.split() if s.isdigit()]
            vol = nums[0] if nums else 50
            return {"action": "set_volume", "param": vol, "response": f"Setting volume to {vol} percent."}
            
        elif "brightness" in cmd_lower:
            nums = [int(s) for s in cmd_lower.split() if s.isdigit()]
            bright = nums[0] if nums else 50
            return {"action": "set_brightness", "param": bright, "response": f"Setting brightness to {bright} percent."}
            
        elif "open" in cmd_lower:
            app_name = cmd_lower.split("open", 1)[-1].strip()
            # Remove filler words
            app_name = app_name.replace("the", "").replace("app", "").strip()
            return {"action": "open_app", "param": app_name, "response": f"Opening {app_name} for you, boss."}
            
        elif "play" in cmd_lower and ("music" in cmd_lower or "song" in cmd_lower or "youtube" in cmd_lower):
            song_name = cmd_lower.split("play", 1)[-1].strip()
            return {"action": "play_music", "param": song_name, "response": f"Playing {song_name} on YouTube."}
            
        elif "sleep" in cmd_lower and ("pc" in cmd_lower or "computer" in cmd_lower or "system" in cmd_lower):
             return {"action": "system_action", "param": "sleep", "response": "Putting the PC to sleep now."}
             
        elif "shutdown" in cmd_lower or "shut down" in cmd_lower:
             return {"action": "system_action", "param": "shutdown", "response": "Shutting down the system."}

        # --- ONLINE AI PARSING FOR COMPLEX QUERIES ---
        if not self.available:
            return {
                "action": "chat", 
                "param": "", 
                "response": "Boss, I am currently offline and cannot understand complex questions. But I can still control your PC if you give direct commands like 'Open Chrome' or 'Set volume to 50'."
            }
            
        try:
            res = self.co.chat(
                model=Config.AI_MODEL,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": command}
                ],
                temperature=0.3
            )
            text = res.message.content[0].text
            
            # Simple fallback extraction
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                return data
                
            # If JSON parsing completely fails but we got text
            return {"action": "chat", "param": "", "response": text}
            
        except Exception as e:
            logger.error(f"Error handling command: {e}")
            return {"action": "chat", "param": "", "response": "Whoops, I burnt the patty. Something went wrong!"}
