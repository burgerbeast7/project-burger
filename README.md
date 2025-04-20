# 🍔 Burger Bot - AI Voice & Text Chatbot 

**Burger Bot** is an AI-powered voice and text chatbot. It uses the **Cohere AI API** for generating intelligent conversational responses, combined with Python's `SpeechRecognition`, `pyttsx3`, and a modern PyQt5 GUI for an engaging user experience. It also comes with **built-in assistant commands** like opening apps and websites.

---

## 🧠 Features

- 🎤 **Voice Input**: Powered by `SpeechRecognition`
- 🗣️ **Voice Output**: Enabled via `pyttsx3`
- 💬 **Conversational AI**: Built using [Cohere](https://cohere.com/)
- 💻 **Modern GUI**: Designed with PyQt5
- 🔄 **Seamless Interaction**: Supports both text and voice
- 🧭 **Personal Assistant**: Can open apps like YouTube, Calculator, Browser, and more
- 🔐 **Secure API Key Usage**
- 🌐 **Lightweight**: Internet-based, no heavy local models required

---

## 🛠️ Tech Stack

- **Python** 3.12
- **PyQt5**
- **Cohere API** (via `cohere` Python SDK)
- **SpeechRecognition**
- **Pyttsx3**

---

## 📁 Project Structure

burger-bot/ ├── main.py # GUI launcher ├── burger_voice.py # Voice I/O and assistant commands ├── chatbot_engine.py # Cohere integration logic ├── config.py # API key handling ├── requirements.txt # Dependencies ├── ui/ # UI files (optional) └── assets/ # Icons, audio, etc.

yaml
Copy
Edit

---

## 🔧 Installation & Setup

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/your-username/burger-bot
    cd burger-bot
    ```

2. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Add Your Cohere API Key**:

    Create a `config.py` file and add the following:

    ```python
    COHERE_API_KEY = "your-cohere-api-key-here"
    ```

    > 🔐 **Note**: Never share this key publicly. Use `.gitignore` to protect it.

4. **Run the App**:

    ```bash
    python main.py
    ```

---

## 🧠 What is Cohere?

[Cohere](https://cohere.com) provides large language models for various NLP tasks such as text generation, classification, summarization, and more. It’s similar to OpenAI but offers its own unique models and a generous free tier.

---

## 🚀 Current Capabilities & Future Scope

### ✅ Already Implemented:
- Voice and text-based interaction
- Natural language response generation via Cohere
- Open system apps like **YouTube, Calculator, Browser**, etc.

### 🔮 Planned Features:
- Enhanced context memory
- Offline fallback model
-  animations and sounds
- Web-based UI version

---

## 🙋‍♂️ Author

**Kunal Chauhan**  


---

## 📄 License
