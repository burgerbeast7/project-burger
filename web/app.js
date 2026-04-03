/* Burger Bot Web App - Logic & Voice Engine */

const statusText = document.getElementById('status-text');
const subStatusText = document.getElementById('sub-status');
const burgerChar = document.getElementById('burger-character');
const thinkingDots = document.getElementById('thinking-dots');
const chatBubble = document.getElementById('chat-bubble');
const chatText = document.getElementById('chat-text');
const micBtn = document.getElementById('mic-btn');

// --- APP STATE ---
let isListening = false;
let isSpeaking = false;
let isThinking = false;

// --- CONFIG ---
// Automatically detect the base URL from the current browser address
const API_BASE = window.location.origin; 
console.log("🍔 Burger Web Engine pointing to:", API_BASE);

// --- VOICE ENGINE ---
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = SpeechRecognition ? new SpeechRecognition() : null;

if (recognition) {
  recognition.lang = 'en-IN'; // Good for English/Hindi/Hinglish
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onstart = () => {
    updateState('listening', 'Listening...');
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    processQuery(transcript);
  };

  recognition.onerror = (event) => {
    console.error('Speech Recognition Error:', event.error);
    updateState('idle', 'Oops, try again!');
  };

  recognition.onend = () => {
    if (!isThinking) {
      updateState('idle', 'Tap to speak');
    }
  };
} else {
  alert('Speech Recognition is not supported in this browser. Try Chrome or Safari.');
}

// --- CORE LOGIC ---

async function processQuery(text) {
  updateState('thinking', 'Processing...');
  showChat(text); 

  try {
    const response = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text })
    });

    const data = await response.json();
    handleResponse(data);

  } catch (error) {
    console.error('Fetch Error:', error);
    updateState('idle', 'Server connect failed!');
    speak("I can't reach my local brain, Boss.");
  }
}

function handleResponse(data) {
  const response = data.response || "I'm not sure what happened!";
  showChat(response);
  speak(response);
}

function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = 1.0;
    
    utterance.onstart = () => {
        updateState('speaking', 'Speaking...');
    };
    
    utterance.onend = () => {
        updateState('idle', 'Ready for more');
    };

    window.speechSynthesis.speak(utterance);
}

// --- UI UPDATES ---

function updateState(state, text) {
  statusText.innerText = text;
  
  // Clear classes
  burgerChar.classList.remove('listening', 'thinking', 'speaking', 'idle');
  thinkingDots.classList.add('hidden');
  micBtn.classList.remove('listening');

  if (state === 'listening') {
    isListening = true;
    isThinking = false;
    burgerChar.classList.add('listening');
    micBtn.classList.add('listening');
  } else if (state === 'thinking') {
    isListening = false;
    isThinking = true;
    burgerChar.classList.add('thinking');
    thinkingDots.classList.remove('hidden');
  } else if (state === 'speaking') {
    isSpeaking = true;
    burgerChar.classList.add('speaking');
  } else {
    isListening = false;
    isThinking = false;
    isSpeaking = false;
    burgerChar.classList.add('idle');
  }
}

function showChat(text) {
  chatBubble.classList.remove('hidden');
  chatText.innerText = text;
  
  // Auto-hide bubble after speech if too long
  setTimeout(() => {
    if (!isSpeaking && !isThinking) {
        // chatBubble.classList.add('hidden');
    }
  }, 5000);
}

// --- EVENT LISTENERS ---

micBtn.addEventListener('click', () => {
  if (isListening) {
    recognition.stop();
  } else if (!isThinking) {
    recognition.start();
  }
});

// Load Settings on Start
window.addEventListener('load', async () => {
    try {
        const res = await fetch(`${API_BASE}/settings`);
        const profile = await res.json();
        subStatusText.innerText = `Connected to ${profile.assistant_name}`;
        showChat(`Hii ${profile.user_name}, I'm ready!`);
    } catch (e) {
        subStatusText.innerText = "Check local server!";
    }
});
