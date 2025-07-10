#!/usr/bin/env python3
"""
Test script for OCR detection and TTS functionality
"""

import sys
import logging
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from ocr_detector import OCRDetector
from tts_handler import TTSHandler

def test_ocr():
    """Test OCR detection"""
    print("\\n=== Testing OCR Detection ===")
    
    detector = OCRDetector()
    print("OCR Detector initialized")
    
    # Test detection
    result = detector.test_detection()
    print(f"Detection result: {result}")
    
def test_tts():
    """Test TTS functionality"""
    print("\\n=== Testing TTS ===")
    
    tts = TTSHandler()
    if tts.tts_engine:
        print("TTS Engine available")
        tts.test_tts()
    else:
        print("TTS Engine not available")

def main():
    """Main test function"""
    logging.basicConfig(level=logging.INFO)
    
    print("DbD Communication App - Test Script")
    print("==================================")
    
    try:
        test_ocr()
        test_tts()
    except Exception as e:
        print(f"Test failed: {e}")
        return 1
        
    print("\\nTest completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
