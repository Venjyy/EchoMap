#!/usr/bin/env python3
"""
Setup script for DbD Communication App
"""

import sys
import subprocess
from pathlib import Path

def install_requirements():
    """Install required Python packages"""
    try:
        print("Installing Python requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False

def check_tesseract():
    """Check if Tesseract is installed"""
    try:
        subprocess.check_call(["tesseract", "--version"], 
                            stdout=subprocess.DEVNULL, 
                            stderr=subprocess.DEVNULL)
        print("✓ Tesseract OCR is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Tesseract OCR not found")
        print("  Please install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki")
        return False

def create_directories():
    """Create necessary directories"""
    dirs = ["maps", "config", "screenshots", "logs"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✓ Created directory: {dir_name}")

def create_placeholder_map():
    """Create a placeholder map image"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create placeholder image
        width, height = 800, 600
        image = Image.new('RGB', (width, height), color='#2C2C2C')
        draw = ImageDraw.Draw(image)
        
        # Draw text
        text = "PLACEHOLDER MAP"
        subtext = "Place your DbD map images in /maps/ folder"
        
        try:
            font = ImageFont.truetype("arial.ttf", 36)
            small_font = ImageFont.truetype("arial.ttf", 18)
        except OSError:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Center the text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (width - text_width) // 2
        text_y = (height - text_height) // 2 - 30
        
        bbox_sub = draw.textbbox((0, 0), subtext, font=small_font)
        subtext_width = bbox_sub[2] - bbox_sub[0]
        subtext_x = (width - subtext_width) // 2
        subtext_y = text_y + text_height + 20
        
        draw.text((text_x, text_y), text, fill='white', font=font)
        draw.text((subtext_x, subtext_y), subtext, fill='#CCCCCC', font=small_font)
        
        # Save placeholder
        placeholder_path = Path("maps") / "placeholder_map.jpg"
        image.save(placeholder_path)
        print(f"✓ Created placeholder image: {placeholder_path}")
        
    except ImportError:
        print("⚠ PIL not available, skipping placeholder creation")
    except Exception as e:
        print(f"✗ Error creating placeholder: {e}")

def main():
    """Main setup function"""
    print("DbD Communication App - Setup")
    print("=" * 40)
    
    success = True
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        success = False
    
    # Check Tesseract
    if not check_tesseract():
        success = False
        
    # Create placeholder map
    create_placeholder_map()
    
    print("\\n" + "=" * 40)
    if success:
        print("✓ Setup completed successfully!")
        print("\\nNext steps:")
        print("1. Place DbD map images in the /maps/ folder")
        print("2. Run 'python main.py' to start the application")
        print("3. Run 'python test.py' to test OCR and TTS")
    else:
        print("✗ Setup completed with errors")
        print("Please resolve the issues above before running the application")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
