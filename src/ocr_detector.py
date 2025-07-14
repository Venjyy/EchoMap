#!/usr/bin/env python3
"""
OCR Detector for Dead by Daylight Map Names
"""

import logging
import time
from pathlib import Path
import pyautogui
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import json


class OCRDetector:
    """Handles OCR detection of map names from screenshots"""

    def __init__(self, config_path="config/ocr_config.json"):
        self.logger = logging.getLogger(__name__)
        self.config_path = Path(config_path)
        self.config = self.load_config()

        # Set tesseract path if specified in config
        if self.config.get("tesseract_path"):
            pytesseract.pytesseract.tesseract_cmd = self.config["tesseract_path"]

        # Screenshot settings
        self.screenshot_region = self.config.get(
            "screenshot_region", (50, 850, 400, 950))
        self.confidence_threshold = self.config.get(
            "confidence_threshold", 0.7)

        # Map name mappings for OCR corrections
        self.map_mappings = self.config.get("map_mappings", {})

    def load_config(self):
        """Load OCR configuration"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Create default config
                default_config = self.create_default_config()
                self.save_config(default_config)
                return default_config
        except Exception as e:
            self.logger.error("Error loading OCR config: %s", e)
            return self.create_default_config()

    def create_default_config(self):
        """Create default OCR configuration"""
        return {
            "tesseract_path": "",  # Leave empty for system PATH
            "screenshot_region": [50, 850, 400, 950],  # x1, y1, x2, y2
            "confidence_threshold": 0.7,
            "preprocessing": {
                "contrast_factor": 2.0,
                "brightness_factor": 1.2,
                "apply_gaussian_blur": True,
                "blur_radius": 0.5
            },
            "tesseract_config": "--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ",
            "map_mappings": {
                # OCR corrections for common misreads
                "haddonfield": "Haddonfield",
                "springwood": "Springwood",
                "macmillan": "MacMillan Estate",
                "autohaven": "Autohaven Wreckers",
                "coldwind": "Coldwind Farm",
                "crotus": "Crotus Prenn Asylum",
                "backwater": "Backwater Swamp",
                "lery": "Léry's Memorial Institute",
                "thegame": "The Game",
                "thehospital": "The Hospital",
                "redforest": "Red Forest",
                "yamaoka": "Yamaoka Estate",
                "ormond": "Ormond",
                "hawkins": "Hawkins National Laboratory",
                "midwich": "Midwich Elementary School",
                "silent": "Silent Hill",
                "raccoon": "Raccoon City Police Station",
                "rpd": "Raccoon City Police Station",
                "eyrie": "Eyrie of Crows",
                "garden": "Garden of Joy",
                "shattered": "Shattered Square",
                "toba": "Toba Landing",
                "dvarka": "Dvarka Deepwood",
                "nostromo": "Nostromo Wreckage",
                "forgotten": "Forgotten Ruins"
            }
        }

    def save_config(self, config):
        """Save configuration to file"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error("Error saving OCR config: %s", e)

    def take_screenshot(self, region=None):
        """Take screenshot of specified region"""
        try:
            if region is None:
                region = self.screenshot_region

            screenshot = pyautogui.screenshot(region=region)

            # Save screenshot for debugging
            timestamp = int(time.time())
            screenshot_path = Path("screenshots") / \
                f"map_detection_{timestamp}.png"
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            screenshot.save(screenshot_path)

            return screenshot
        except Exception as e:
            self.logger.error("Error taking screenshot: %s", e)
            return None

    def preprocess_image(self, image):
        """Preprocess image for better OCR accuracy"""
        try:
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')

            preprocessing = self.config.get("preprocessing", {})

            # Enhance contrast
            contrast_factor = preprocessing.get("contrast_factor", 2.0)
            if contrast_factor != 1.0:
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(contrast_factor)

            # Enhance brightness
            brightness_factor = preprocessing.get("brightness_factor", 1.2)
            if brightness_factor != 1.0:
                enhancer = ImageEnhance.Brightness(image)
                image = enhancer.enhance(brightness_factor)

            # Apply Gaussian blur to reduce noise
            if preprocessing.get("apply_gaussian_blur", True):
                blur_radius = preprocessing.get("blur_radius", 0.5)
                image = image.filter(
                    ImageFilter.GaussianBlur(radius=blur_radius))

            return image
        except Exception as e:
            self.logger.error("Error preprocessing image: %s", e)
            return image

    def extract_text_from_image(self, image):
        """Extract text from image using OCR"""
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image)

            # OCR configuration
            tesseract_config = self.config.get("tesseract_config", "--psm 8")

            # Extract text
            text = pytesseract.image_to_string(
                processed_image, config=tesseract_config)

            # Clean up text
            text = text.strip().replace('\\n', ' ').replace('\\r', ' ')
            text = ' '.join(text.split())  # Remove extra whitespace

            return text
        except Exception as e:
            self.logger.error("Error extracting text from image: %s", e)
            return ""

    def normalize_map_name(self, raw_text):
        """Normalize and correct OCR-detected text to actual map name"""
        if not raw_text:
            return None

        # Convert to lowercase for comparison
        text_lower = raw_text.lower()

        # Check direct mappings first
        for key, value in self.map_mappings.items():
            if key in text_lower:
                return value

        # Check for partial matches
        for key, value in self.map_mappings.items():
            if any(word in text_lower for word in key.split()):
                return value

        # If no mapping found, return cleaned original
        return raw_text.title()

    def detect_map(self):
        """Main method to detect current map name"""
        try:
            # Take screenshot
            screenshot = self.take_screenshot()
            if screenshot is None:
                return None

            # Extract text
            raw_text = self.extract_text_from_image(screenshot)
            if not raw_text:
                return None

            self.logger.debug("Raw OCR text: '%s'", raw_text)

            # Normalize map name
            map_name = self.normalize_map_name(raw_text)

            if map_name:
                self.logger.info("Detected map: %s", map_name)
                return map_name
            else:
                self.logger.debug(
                    "No valid map name detected from: '%s'", raw_text)
                return None

        except Exception as e:
            self.logger.error("Error detecting map: %s", e)
            return None

    def update_screenshot_region(self, x1, y1, x2, y2):
        """Update the screenshot region coordinates"""
        self.screenshot_region = (x1, y1, x2, y2)
        self.config["screenshot_region"] = [x1, y1, x2, y2]
        self.save_config(self.config)

    def test_detection(self):
        """Test method for debugging OCR detection"""
        self.logger.info("Testing OCR detection...")

        screenshot = self.take_screenshot()
        if screenshot:
            raw_text = self.extract_text_from_image(screenshot)
            map_name = self.normalize_map_name(raw_text)

            print(f"Raw text: '{raw_text}'")
            print(f"Detected map: '{map_name}'")

            return map_name
        return None
