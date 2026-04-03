<p align="center">
  <img src="burger-bot/burger_app_screenshot.png" width="300" alt="Burger AI Logo">
</p>

# <div align="center">🍔 BURGER AI – Your Animated Desktop Companion</div>

<div align="center">

> Meet the futuristic, frameless, floating AI desktop assistant that brings intelligence and automation to your local system in a fun & animated way!

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![Cohere](https://img.shields.io/badge/Cohere-AI-purple?style=for-the-badge&logo=cohere)](https://cohere.com/)
[![Windows](https://img.shields.io/badge/Windows-Supported-0078D6?style=for-the-badge&logo=windows)](https://microsoft.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)](#)

</div>
<br/>

## 🌟 What is BURGER AI?

**BURGER AI** is an advanced voice-activated desktop assistant designed to hover dynamically on your screen. Not just a chatbot, BURGER features a **transparent, frameless UI** and real-time animations. Powered by **Cohere's command-r-08-2024**, BURGER processes your natural language, automates complex local OS actions, and effortlessly switches between English, Hindi, and Hinglish. 

---

## ⚡ Core Features

### 🎨 1. Living Character UI
BURGER isn't just text on a terminal. He lives on your screen.
- **Frameless & Transparent:** Casts a floating presence directly over your active windows without getting in the way.
- **Smart Animations:** Modifies expressions dynamically—**Idle** (blinking), **Listening** (glowing aura), **Thinking** (loading indicator), and **Speaking** (lip-syncing).

### 🤖 2. Intelligent Multi-lingual Brain 
Powered by Cohere AI, BURGER's brain understands deep context without missing a beat:
- Extracts exact intents via JSON schema directly from conversational prompts.
- Fluent in **English**, **Hindi**, and **Hinglish** (e.g., *"Burger, mera volume kam kar do"*).

### 🎙️ 3. Fully Voice Driven
Keep your hands on the keyboard for real work.
- **Always Listening:** Wake word activated ("Burger").
- Uses **Google Speech API (`en-IN`)** for high-accuracy local dialect transcription.
- Features **Fast Windows SAPI TTS** for instant, thread-safe speech synthesis to reply aloud.

### ⚙️ 4. Blazing Fast OS Automation
Bypasses cloud latency when executing local system commands:
- **App Launching:** *"Open Chrome"*, *"Launch VS Code"*
- **System Controls:** *"Set volume to 40%”*, *"Increase brightness"*, *"Sleep PC"*
- **Entertainment:** *"Play relaxed lo-fi music"* (Auto-searches & opens YouTube seamlessly).

---

## 🏗️ System Architecture

| Component | Responsibility |
|---|---|
| 🧠 **`main.py`** | Core orchestrator bridging background services (voice, commands, UI threads). |
| 👁️ **`character_ui.py`** | Custom Tkinter/Canvas GUI managing animations, physics, and alpha-channels. |
| 🎤 **`voice_engine.py`** | Background audio processing, localized SpeechRecognition, and TTS. |
| 🧩 **`command_handler.py`** | Dual-layer NLP routing (Fast Regex for local actions + Cohere API for abstract thinking). |
| 🔌 **`automation.py`** | Python OS interface for system controls, external web APIs, and application linking. |
| 🔒 **`config.py`** | Central configuration and environment variable mappings (API Keys). |

---

## 🚀 Getting Started

Transform your desktop in minutes. Here's how:

### Prerequisites
- Windows 10/11 OS (Required for transparent GUI mode)
- Python 3.9+
- A [Cohere API Key](https://cohere.com/) (Free tier works perfectly!)
- Working Microphone & Speakers

### Installation Steps

**1. Clone the Repository:**
```bash
git clone https://github.com/burgerbeast7/project-burger.git
cd project-burger
```

**2. Create & Activate a Virtual Environment:**
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
```

**3. Install Dependencies:**
```bash
pip install -r burger-bot/requirements.txt
```

**4. Set Up Configuration:**
Create a `.env` file in the `burger-bot/` directory with your API key:
```env
COHERE_API_KEY=your_cohere_api_key_here
```

**5. Wake Him Up!:**
```bash
python burger-bot/main.py
```

<br/>

## 🗣️ Interactive Examples

Try these out once BURGER is ready on your screen!

> **You:** "Burger, what's up?" <br>
> **🤖 BURGER:** "Hii boss, nothing much, what can I do for you?" 

> **You:** "Mera volume kam kar do please." <br>
> **🤖 BURGER:** (Decreases system volume) "Volume set to lower level."

> **You:** "Burger, open Chrome." <br>
> **🤖 BURGER:** "Right away, opening Chrome!"

---

## 🛠️ Contributing

Got ideas to make BURGER even cooler? 
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingIdea`)
3. Commit your Changes (`git commit -m 'Added Super Cool Feature'`)
4. Push to the Branch (`git push origin feature/AmazingIdea`)
5. Open a Pull Request

---

<div align="center">
  <p><b>Built with ❤️ by Burgerbeast7</b></p>
  <i>"Let your PC talk to you."</i>
</div>
