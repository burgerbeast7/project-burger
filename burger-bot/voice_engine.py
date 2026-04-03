import speech_recognition as sr
import threading
import logging
import time
import random
import os
from gtts import gTTS
import pygame
import random


logger = logging.getLogger(__name__)

class VoiceEngine:
    def __init__(self, state_callback, process_command_callback):
        self.state_callback = state_callback
        self.process_command_callback = process_command_callback
        self.recognizer = sr.Recognizer()
        
        # Initialize pygame mixer for fast audio playback
        pygame.mixer.init()
        
        self.is_running = False
        self._listen_thread = None

    def start(self):
        self.is_running = True
        self._listen_thread = threading.Thread(target=self._background_listen, daemon=True)
        self._listen_thread.start()

    def speak(self, text):
        """Speak text using Professional Cloud TTS and change UI state to SPEAKING."""
        self.state_callback("SPEAKING", text)
        try:
            # Create a professional cloud voice with accurate Hinglish accent
            tts = gTTS(text=text, lang='en', tld='co.in')
            filename = "temp_burger_speech.mp3"
            
            # Save and play the audio using pygame
            tts.save(filename)
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            # Wait for audio to finish so UI syncs
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
            # Unload the file so it can be overwritten next time
            pygame.mixer.music.unload()
            
        except Exception as e:
            logger.error(f"Cloud TTS Error: {e}")
            
        # Give a small pause before going idle
        time.sleep(0.2)
        self.state_callback("IDLE", "Sleeping...")

    def _background_listen(self):
        """Continuous listening loop looking for wake word."""
        with sr.Microphone() as source:
            logger.info("Adjusting for ambient noise...")
            self.state_callback("IDLE", "Calibrating...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
            self.state_callback("IDLE", "Sleeping... (Say 'Burger')")
            
            while self.is_running:
                try:
                    # Listen for quick bursts (the wake word)
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=4)
                    text = self.recognizer.recognize_google(audio, language="en-IN").lower()
                    
                    if "burger" in text:
                        # Wake word detected! Let's handle it
                        self.state_callback("LISTENING", "Yes?")
                        
                        # Did the user say the command in the same breath?
                        command = text.split("burger", 1)[-1].strip()
                        
                        # If just said "Burger", listen again for the actual command
                        if not command:
                            ack = random.choice(["Yes boss?", "I'm listening.", "Yes?", "Hmm?"])
                            self.speak(ack)
                            self.state_callback("LISTENING", "Listening for command...")
                            try:
                                audio_cmd = self.recognizer.listen(source, timeout=4, phrase_time_limit=10)
                                command = self.recognizer.recognize_google(audio_cmd, language="en-IN")
                            except:
                                command = ""
                                
                        if command:
                            self.state_callback("THINKING", "Processing...")
                            # Send command to handler
                            self.process_command_callback(command)
                        else:
                            self.state_callback("IDLE", "Sleeping...")
                            
                except sr.WaitTimeoutError:
                    # Expected timeout when nobody is speaking
                    pass
                except sr.UnknownValueError:
                    # Could not understand audio (mumbling)
                    pass
                except Exception as e:
                    # Might happen if mic is disconnected
                    pass
