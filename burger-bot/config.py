import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'burger-bot-secret-2026'
    DEBUG = os.environ.get('DEBUG', 'True').lower() in ['true', '1', 't']

    # AI Configuration (Cohere)
    COHERE_API_KEY = os.environ.get('COHERE_API_KEY', '')
    AI_MODEL = os.environ.get('AI_MODEL', 'command-r-08-2024')
    DEFAULT_PERSONALITY = os.environ.get('DEFAULT_PERSONALITY', 'assistant')

    # Chat Settings
    MAX_CONTEXT_MESSAGES = int(os.environ.get('MAX_CONTEXT_MESSAGES', '20'))
    CHAT_HISTORY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chat_history')

    # File Upload Settings
    MAX_FILE_SIZE_MB = 10
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')