# 🍔 BURGER AI — Animated Desktop Assistant

> A living, animated, floating Burger character that serves as your futuristic AI desktop companion. Understands English, Hindi, and Hinglish!

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Cohere](https://img.shields.io/badge/Cohere-AI-purple)

## ✨ Features

### 🍔 Living Character UI
- **Frameless & Transparent:** Floating directly on top of your desktop windows.
- **Dynamic Animations:**
  - `IDLE`: Hovers gently and blinks.
  - `LISTENING`: Glowing aura behind him.
  - `THINKING`: Squints with a futuristic loading orb spinning over his head.
  - `SPEAKING`: Mouth fully animates to his speech.

### ⚡ Blazing Fast OS Automation (Offline Capable)
BURGER intercepts system commands instantaneously without relying on the cloud for:
- `"Open Chrome"`, `"Open VS Code"`, etc.
- `"Set volume to 40"`
- `"Set brightness to 80"`
- `"Play relaxing music"` (Auto-finds and plays in YouTube)
- `"Sleep PC"`, `"Shutdown"`

### 🧠 Smart Cohere Brain (Online Mode)
- Deeply integrates with **Cohere's command-r-08-2024** for multi-language understanding.
- Understands **English**, **Hindi**, and **Hinglish**.
- Extracts JSON-based intentions accurately for web searches or natural conversation.

### 🎤 Voice Driven (No Typing)
- **Always Listening:** Say **"Burger"** to wake him up.
- **Windows SAPI TTS:** Fast, thread-safe, native speech synthesis.
- **Microphone Inputs:** Uses Google Speech API localized to `en-IN` (Indian English) for phenomenal Hinglish transcription.

## 🚀 How to Run

1. **Install Dependencies**
   ```bash
   pip install pyttsx3 SpeechRecognition pywhatkit AppOpener screen-brightness-control pycaw comtypes pyaudio cohere
   ```

2. **Run BURGER**
   ```bash
   python main.py
   ```
   *You'll see him immediately appear floating on your desktop!*

3. **Say Hi!**
   Just speak into your mic: 
   > *"Burger, what can you do?"*
   > *Wait for response*
   > *"Burger, open YouTube."*

## 📁 System Architecture
- `main.py` - Core orchestrator & threading logic.
- `character_ui.py` - Tkinter transparent Canvas with trig-based animations.
- `voice_engine.py` - Background SAPI and SpeechRecognition loops.
- `command_handler.py` - Dual-layer parsing (Fast Local Keyword regex + Cohere AI).
- `automation.py` - Native OS controllers and PyWhatKit integrations.