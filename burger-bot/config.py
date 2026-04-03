import os
import json
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    USER_PROFILE_PATH = os.path.join(BASE_DIR, 'user_profile.json')
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'burger-bot-secret-2026'
    DEBUG = os.environ.get('DEBUG', 'True').lower() in ['true', '1', 't']

    # AI Configuration (Cohere)
    COHERE_API_KEY = os.environ.get('COHERE_API_KEY', '')
    AI_MODEL = os.environ.get('AI_MODEL', 'command-r-08-2024')
    DEFAULT_PERSONALITY = os.environ.get('DEFAULT_PERSONALITY', 'assistant')

    # Chat Settings
    MAX_CONTEXT_MESSAGES = int(os.environ.get('MAX_CONTEXT_MESSAGES', '20'))
    CHAT_HISTORY_DIR = os.path.join(BASE_DIR, 'chat_history')

    # File Upload Settings
    MAX_FILE_SIZE_MB = 10
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

    @classmethod
    def get_user_profile(cls):
        """Load profile from JSON, fallback to default if not exists."""
        if os.path.exists(cls.USER_PROFILE_PATH):
            try:
                with open(cls.USER_PROFILE_PATH, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Default fallback
        return {
            "user_name": "Boss",
            "assistant_name": "BURGER",
            "creator_name": "Kunal Chauhan",
            "personality": "Professional, intelligent, and articulate",
            "hobbies": "Technology, AI, and burgers",
            "language_preference": "Hinglish (Mixed English and Hindi)",
            "cohere_api_key": cls.COHERE_API_KEY
        }

    @classmethod
    def save_user_profile(cls, profile_data):
        """Save profile dict to JSON."""
        try:
            with open(cls.USER_PROFILE_PATH, 'w') as f:
                json.dump(profile_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False