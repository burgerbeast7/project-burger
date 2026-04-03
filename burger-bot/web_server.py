from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
import logging

# Ensure imports work from current dir
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from command_handler import CommandHandler
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'web'))

app = Flask(__name__, static_folder=WEB_DIR, static_url_path='/web')
CORS(app) # Allow cross-origin requests

@app.route('/')
def home():
    """Root access serves the main dashboard."""
    logger.info("Serving index.html to visitor")
    return send_from_directory(WEB_DIR, 'index.html')

@app.route('/<path:path>')
def catch_all(path):
    """Catch-all to serve any other files requested (css, js, icons) from the web folder."""
    return send_from_directory(WEB_DIR, path)

# Initialize the Cohere Brain
cmd_handler = CommandHandler()

@app.route('/chat', methods=['POST'])
def chat():
    """Receive text from web frontend, process via CommandHandler, return response JSON."""
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    user_text = data['text']
    logger.info(f"Web User: {user_text}")
    
    # Use existing CommandHandler (Dynamic Profile aware)
    intent = cmd_handler.process(user_text)
    
    # We return the whole intent (action, param, response)
    # The frontend will decide if it "speaks" or "acts"
    return jsonify(intent)

@app.route('/settings', methods=['GET'])
def get_settings():
    """Expose profile settings to the web frontend for personalization."""
    profile = Config.get_user_profile()
    # Mask API key for security over network
    safe_profile = profile.copy()
    if 'cohere_api_key' in safe_profile:
        safe_profile['cohere_api_key'] = "****"
    return jsonify(safe_profile)

if __name__ == '__main__':
    # Run on 0.0.0.0 so other devices (phones) on the same Wi-Fi can connect!
    logger.info("🍔 Burger Web Server starting on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)
