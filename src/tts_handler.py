#!/usr/bin/env python3
"""
Text-to-Speech Handler for DbD Communication App
"""

import logging
import threading
from queue import Queue


class TTSHandler:
    """Handles text-to-speech functionality"""

    def __init__(self, voice_rate=200, voice_volume=0.9):
        self.logger = logging.getLogger(__name__)
        self.voice_rate = voice_rate
        self.voice_volume = voice_volume
        self.tts_engine = None
        self.speech_queue = Queue()
        self.is_running = False

        self.initialize_tts()

    def initialize_tts(self):
        """Initialize text-to-speech engine"""
        try:
            import pyttsx3

            self.tts_engine = pyttsx3.init()

            # Configure voice settings
            self.tts_engine.setProperty('rate', self.voice_rate)
            self.tts_engine.setProperty('volume', self.voice_volume)

            # Try to set a preferred voice (optional)
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Prefer female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break

            self.logger.info("TTS engine initialized successfully")

        except ImportError:
            self.logger.warning("pyttsx3 not available, TTS disabled")
            self.tts_engine = None
        except Exception as e:
            self.logger.error("Error initializing TTS engine: %s", e)
            self.tts_engine = None

    def start_tts_worker(self):
        """Start TTS worker thread"""
        if not self.is_running and self.tts_engine:
            self.is_running = True
            self.tts_thread = threading.Thread(
                target=self._tts_worker, daemon=True)
            self.tts_thread.start()

    def stop_tts_worker(self):
        """Stop TTS worker thread"""
        self.is_running = False

    def _tts_worker(self):
        """TTS worker thread that processes speech queue"""
        while self.is_running:
            try:
                if not self.speech_queue.empty():
                    text = self.speech_queue.get(timeout=1)
                    if text and self.tts_engine:
                        self.tts_engine.say(text)
                        self.tts_engine.runAndWait()
            except Exception as e:
                self.logger.error("Error in TTS worker: %s", e)

    def speak(self, text):
        """Add text to speech queue"""
        if not text:
            return

        if self.tts_engine:
            if not self.is_running:
                self.start_tts_worker()

            # Clear queue and add new text (interrupt previous speech)
            while not self.speech_queue.empty():
                try:
                    self.speech_queue.get_nowait()
                except:
                    break

            self.speech_queue.put(text)
            self.logger.debug("Added to TTS queue: %s", text)
        else:
            self.logger.debug("TTS not available, would speak: %s", text)

    def speak_callout(self, sector_number, callout_type="sector"):
        """Speak a formatted callout"""
        if callout_type == "killer":
            text = f"Killer in {sector_number}"
        elif callout_type == "rescue":
            text = f"Rescue in {sector_number}"
        elif callout_type == "gen":
            text = f"Generator in {sector_number}"
        elif callout_type == "totem":
            text = f"Totem in {sector_number}"
        else:
            text = f"Sector {sector_number}"

        self.speak(text)

    def test_tts(self):
        """Test TTS functionality"""
        test_phrases = [
            "TTS system online",
            "Killer in sector 3",
            "Rescue in sector 9",
            "Generator complete"
        ]

        for phrase in test_phrases:
            self.speak(phrase)

    def set_voice_rate(self, rate):
        """Set voice speaking rate"""
        self.voice_rate = rate
        if self.tts_engine:
            self.tts_engine.setProperty('rate', rate)

    def set_voice_volume(self, volume):
        """Set voice volume (0.0 to 1.0)"""
        self.voice_volume = max(0.0, min(1.0, volume))
        if self.tts_engine:
            self.tts_engine.setProperty('volume', self.voice_volume)

    def get_available_voices(self):
        """Get list of available voices"""
        if not self.tts_engine:
            return []

        try:
            voices = self.tts_engine.getProperty('voices')
            return [(voice.id, voice.name) for voice in voices] if voices else []
        except Exception as e:
            self.logger.error("Error getting voices: %s", e)
            return []

    def set_voice(self, voice_id):
        """Set specific voice by ID"""
        if self.tts_engine:
            try:
                self.tts_engine.setProperty('voice', voice_id)
                self.logger.info("Voice changed to: %s", voice_id)
            except Exception as e:
                self.logger.error("Error setting voice: %s", e)
