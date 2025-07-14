#!/usr/bin/env python3
"""
Demo script for DbD Communication App
Creates example map images and demonstrates functionality
"""

from map_manager import MapManager
import sys
import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def create_example_maps():
    """Create example map images for demonstration"""
    maps_dir = Path("maps")
    maps_dir.mkdir(exist_ok=True)

    # Example map names and colors
    example_maps = [
        ("haddonfield.jpg", "Haddonfield", "#4A4A4A"),
        ("springwood.jpg", "Springwood", "#8B4513"),
        ("macmillan.jpg", "MacMillan Estate", "#2F4F4F"),
        ("autohaven.jpg", "Autohaven Wreckers", "#696969"),
        ("coldwind.jpg", "Coldwind Farm", "#556B2F")
    ]

    for filename, map_name, color in example_maps:
        map_path = maps_dir / filename
        if not map_path.exists():
            create_map_image(map_path, map_name, color)
            print(f"Created example map: {filename}")


def create_map_image(path, map_name, bg_color="#2C2C2C"):
    """Create a sample map image"""
    width, height = 800, 600
    image = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)

    # Try to load font
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        subtitle_font = ImageFont.truetype("arial.ttf", 24)
    except OSError:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    # Draw map name
    bbox = draw.textbbox((0, 0), map_name, font=title_font)
    text_width = bbox[2] - bbox[0]
    text_x = (width - text_width) // 2
    text_y = height // 2 - 50

    draw.text((text_x, text_y), map_name, fill='white', font=title_font,
              stroke_width=2, stroke_fill='black')

    # Draw subtitle
    subtitle = "Example Map Image"
    bbox_sub = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    sub_width = bbox_sub[2] - bbox_sub[0]
    sub_x = (width - sub_width) // 2
    sub_y = text_y + 80

    draw.text((sub_x, sub_y), subtitle, fill='#CCCCCC', font=subtitle_font)

    # Draw some example structures
    # Main building (center)
    draw.rectangle([350, 250, 450, 350], fill='#8B4513',
                   outline='white', width=2)

    # Generator locations (corners)
    gen_positions = [(100, 100), (700, 100), (100, 500), (700, 500)]
    for x, y in gen_positions:
        draw.ellipse([x-15, y-15, x+15, y+15], fill='yellow',
                     outline='orange', width=2)

    # Exit gates
    draw.rectangle([380, 50, 420, 70], fill='red', outline='darkred', width=2)
    draw.rectangle([380, 530, 420, 550], fill='red',
                   outline='darkred', width=2)

    image.save(path)


def demo_functionality():
    """Demonstrate app functionality without full GUI"""
    print("\\n=== DbD Communication App Demo ===")

    # Test Map Manager
    print("\\nTesting Map Manager...")
    map_manager = MapManager()
    available_maps = map_manager.get_available_maps()
    print(f"Available maps: {available_maps}")

    if available_maps:
        test_map = available_maps[0]
        map_path = map_manager.get_map_image(test_map)
        print(f"Map image path for '{test_map}': {map_path}")

    # Create placeholder if needed
    placeholder_path = Path("maps") / "placeholder_map.jpg"
    if not placeholder_path.exists():
        map_manager.create_placeholder_image()
        print("Created placeholder image")


def main():
    """Main demo function"""
    logging.basicConfig(level=logging.INFO)

    print("DbD Communication App - Demo")
    print("===========================")

    try:
        # Create example maps
        print("Creating example map images...")
        create_example_maps()

        # Demonstrate functionality
        demo_functionality()

        print("\\n✓ Demo completed successfully!")
        print("\\nTo run the full application:")
        print("python main.py")

    except Exception as e:
        print(f"Demo failed: {e}")
        logging.error("Demo error", exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
