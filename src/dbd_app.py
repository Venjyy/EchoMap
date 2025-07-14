#!/usr/bin/env python3
"""
DbD Communication App - Main Application Class
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import logging
from pathlib import Path

from ocr_detector import OCRDetector
from map_manager import MapManager
from gui_interface import MapGUI
from tts_handler import TTSHandler


class DbDCommunicationApp:
    """Main application class for DbD Communication App"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.root = tk.Tk()
        self.root.title("DbD Communication App")
        self.root.geometry("800x600")

        # Initialize components
        self.ocr_detector = OCRDetector()
        self.map_manager = MapManager()
        self.tts_handler = TTSHandler()
        self.map_gui = None

        # Application state
        self.current_map = None
        self.detection_active = False
        self.detection_thread = None

        self.setup_main_interface()

    def setup_main_interface(self):
        """Setup the main control interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Title
        title_label = ttk.Label(main_frame, text="DbD Communication App",
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2,
                          sticky="ew", pady=(0, 10))

        self.status_label = ttk.Label(status_frame, text="Ready to detect map")
        self.status_label.grid(row=0, column=0, sticky="w")

        self.current_map_label = ttk.Label(status_frame, text="No map detected",
                                           font=("Arial", 10, "italic"))
        self.current_map_label.grid(row=1, column=0, sticky="w")

        # Control buttons frame
        control_frame = ttk.LabelFrame(
            main_frame, text="Controls", padding="10")
        control_frame.grid(row=2, column=0, columnspan=2,
                           sticky="ew", pady=(0, 10))

        # Detection toggle button
        self.detection_button = ttk.Button(control_frame, text="Start Detection",
                                           command=self.toggle_detection)
        self.detection_button.grid(row=0, column=0, padx=(0, 10))

        # Manual map selection
        ttk.Label(control_frame, text="Manual map:").grid(
            row=0, column=1, padx=(10, 5))

        self.map_var = tk.StringVar()
        self.map_combo = ttk.Combobox(control_frame, textvariable=self.map_var,
                                      values=self.map_manager.get_available_maps(),
                                      state="readonly", width=25)
        self.map_combo.grid(row=0, column=2, padx=(0, 10))

        ttk.Button(control_frame, text="Load Map",
                   command=self.load_selected_map).grid(row=0, column=3)

        # Settings frame
        settings_frame = ttk.LabelFrame(
            main_frame, text="Settings", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=2,
                            sticky="ew", pady=(0, 10))

        # Sector mode selection
        ttk.Label(settings_frame, text="Sector Mode:").grid(
            row=0, column=0, sticky="w")

        self.sector_mode = tk.StringVar(value="clock")
        ttk.Radiobutton(settings_frame, text="12-Hour Clock", variable=self.sector_mode,
                        value="clock").grid(row=0, column=1, sticky="w", padx=(10, 0))
        ttk.Radiobutton(settings_frame, text="9-Zone Numpad", variable=self.sector_mode,
                        value="numpad").grid(row=0, column=2, sticky="w", padx=(10, 0))

        # TTS enable/disable
        self.tts_enabled = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Enable Text-to-Speech",
                        variable=self.tts_enabled).grid(row=1, column=0, columnspan=3, sticky="w", pady=(5, 0))

        # Instructions
        instructions_frame = ttk.LabelFrame(
            main_frame, text="Instructions", padding="10")
        instructions_frame.grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        instructions_text = """1. Start detection to automatically detect maps from screenshots
2. Or manually select a map from the dropdown
3. Click on sectors or use keyboard shortcuts (1-9 or F1-F12)
4. Use callouts like "killer in 3" or "rescue in 9" """

        ttk.Label(instructions_frame, text=instructions_text,
                  justify="left").grid(row=0, column=0, sticky="w")

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def toggle_detection(self):
        """Toggle OCR detection on/off"""
        if not self.detection_active:
            self.start_detection()
        else:
            self.stop_detection()

    def start_detection(self):
        """Start OCR detection in a separate thread"""
        self.detection_active = True
        self.detection_button.config(text="Stop Detection")
        self.status_label.config(
            text="Detection active - monitoring for maps...")

        self.detection_thread = threading.Thread(
            target=self.detection_loop, daemon=True)
        self.detection_thread.start()

    def stop_detection(self):
        """Stop OCR detection"""
        self.detection_active = False
        self.detection_button.config(text="Start Detection")
        self.status_label.config(text="Detection stopped")

    def detection_loop(self):
        """Main detection loop running in background thread"""
        while self.detection_active:
            try:
                detected_map = self.ocr_detector.detect_map()
                if detected_map and detected_map != self.current_map:
                    self.logger.info(f"New map detected: {detected_map}")
                    self.root.after(0, self.on_map_detected, detected_map)

            except Exception as e:
                self.logger.error(f"Error in detection loop: {e}")

            time.sleep(2)  # Check every 2 seconds

    def on_map_detected(self, map_name):
        """Handle when a new map is detected"""
        self.current_map = map_name
        self.current_map_label.config(text=f"Current map: {map_name}")
        self.load_map(map_name)

    def load_selected_map(self):
        """Load manually selected map"""
        selected_map = self.map_var.get()
        if selected_map:
            self.load_map(selected_map)

    def load_map(self, map_name):
        """Load and display a map with sectors"""
        try:
            map_image_path = self.map_manager.get_map_image(map_name)
            if map_image_path:
                # Close existing map window if open
                if self.map_gui:
                    self.map_gui.close()

                # Create new map GUI
                self.map_gui = MapGUI(
                    map_image_path=map_image_path,
                    map_name=map_name,
                    sector_mode=self.sector_mode.get(),
                    tts_handler=self.tts_handler if self.tts_enabled.get() else None
                )
                self.map_gui.show()

                self.logger.info(f"Loaded map: {map_name}")
            else:
                messagebox.showwarning("Map Not Found",
                                       f"Map image for '{map_name}' not found.")

        except Exception as e:
            self.logger.error(f"Error loading map {map_name}: {e}")
            messagebox.showerror("Error", f"Failed to load map: {e}")

    def run(self):
        """Start the application"""
        try:
            self.logger.info("Starting application")
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"Error running application: {e}")
            raise

    def on_closing(self):
        """Handle application closing"""
        self.stop_detection()
        if self.map_gui:
            self.map_gui.close()
        self.root.destroy()
