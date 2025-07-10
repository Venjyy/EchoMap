#!/usr/bin/env python3
"""
Map Manager for Dead by Daylight Maps
"""

import logging
import json
from pathlib import Path

class MapManager:
    """Manages map images and metadata"""
    
    def __init__(self, maps_dir="maps", config_path="config/maps_config.json"):
        self.logger = logging.getLogger(__name__)
        self.maps_dir = Path(maps_dir)
        self.config_path = Path(config_path)
        self.maps_config = self.load_maps_config()
        
        # Ensure maps directory exists
        self.maps_dir.mkdir(parents=True, exist_ok=True)
        
    def load_maps_config(self):
        """Load maps configuration"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Create default config
                default_config = self.create_default_maps_config()
                self.save_maps_config(default_config)
                return default_config
        except Exception as e:
            self.logger.error("Error loading maps config: %s", e)
            return self.create_default_maps_config()
            
    def create_default_maps_config(self):
        """Create default maps configuration"""
        return {
            "maps": {
                "Haddonfield": {
                    "filename": "haddonfield.jpg",
                    "realm": "Haddonfield",
                    "official_name": "Lampkin Lane"
                },
                "Springwood": {
                    "filename": "springwood.jpg", 
                    "realm": "Springwood",
                    "official_name": "Badham Preschool"
                },
                "MacMillan Estate": {
                    "filename": "macmillan.jpg",
                    "realm": "MacMillan Estate", 
                    "official_name": "Coal Tower"
                },
                "Autohaven Wreckers": {
                    "filename": "autohaven.jpg",
                    "realm": "Autohaven Wreckers",
                    "official_name": "Gas Heaven"
                },
                "Coldwind Farm": {
                    "filename": "coldwind.jpg",
                    "realm": "Coldwind Farm",
                    "official_name": "Fractured Cowshed"
                },
                "Crotus Prenn Asylum": {
                    "filename": "crotus.jpg",
                    "realm": "Crotus Prenn Asylum",
                    "official_name": "Disturbed Ward"
                },
                "Backwater Swamp": {
                    "filename": "backwater.jpg",
                    "realm": "Backwater Swamp", 
                    "official_name": "The Pale Rose"
                },
                "Léry's Memorial Institute": {
                    "filename": "lery.jpg",
                    "realm": "Léry's Memorial Institute",
                    "official_name": "Treatment Theatre"
                },
                "The Game": {
                    "filename": "thegame.jpg",
                    "realm": "Gideon Meat Plant",
                    "official_name": "The Game"
                },
                "Red Forest": {
                    "filename": "redforest.jpg",
                    "realm": "Red Forest",
                    "official_name": "Mother's Dwelling"
                },
                "Yamaoka Estate": {
                    "filename": "yamaoka.jpg",
                    "realm": "Yamaoka Estate",
                    "official_name": "Family Residence"
                },
                "Ormond": {
                    "filename": "ormond.jpg",
                    "realm": "Ormond",
                    "official_name": "Mount Ormond Resort"
                },
                "Hawkins National Laboratory": {
                    "filename": "hawkins.jpg",
                    "realm": "Hawkins National Laboratory",
                    "official_name": "Underground Complex"
                },
                "Midwich Elementary School": {
                    "filename": "midwich.jpg",
                    "realm": "Silent Hill",
                    "official_name": "Midwich Elementary School"
                },
                "Raccoon City Police Station": {
                    "filename": "raccoon.jpg",
                    "realm": "Raccoon City",
                    "official_name": "R.P.D. Main Hall"
                },
                "Eyrie of Crows": {
                    "filename": "eyrie.jpg",
                    "realm": "Forsaken Boneyard",
                    "official_name": "Eyrie of Crows"
                },
                "Garden of Joy": {
                    "filename": "garden.jpg",
                    "realm": "Withered Isle",
                    "official_name": "Garden of Joy"
                },
                "Shattered Square": {
                    "filename": "shattered.jpg",
                    "realm": "Withered Isle", 
                    "official_name": "Shattered Square"
                },
                "Toba Landing": {
                    "filename": "toba.jpg",
                    "realm": "Dvarka Deepwood",
                    "official_name": "Toba Landing"
                },
                "Dvarka Deepwood": {
                    "filename": "dvarka.jpg",
                    "realm": "Dvarka Deepwood",
                    "official_name": "Shelter Woods"
                },
                "Nostromo Wreckage": {
                    "filename": "nostromo.jpg",
                    "realm": "Nostromo Wreckage",
                    "official_name": "Nostromo Wreckage"
                },
                "Forgotten Ruins": {
                    "filename": "forgotten.jpg",
                    "realm": "Withered Isle",
                    "official_name": "Forgotten Ruins"
                }
            },
            "placeholders": {
                "enabled": True,
                "default_image": "placeholder_map.jpg"
            }
        }
        
    def save_maps_config(self, config):
        """Save maps configuration to file"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error("Error saving maps config: %s", e)
            
    def get_available_maps(self):
        """Get list of available map names"""
        return list(self.maps_config.get("maps", {}).keys())
        
    def get_map_image(self, map_name):
        """Get path to map image file"""
        maps = self.maps_config.get("maps", {})
        
        if map_name in maps:
            filename = maps[map_name].get("filename")
            if filename:
                image_path = self.maps_dir / filename
                if image_path.exists():
                    return str(image_path)
                else:
                    self.logger.warning("Map image not found: %s", image_path)
                    
        # Try to find by partial name match
        for name, config in maps.items():
            if map_name.lower() in name.lower() or name.lower() in map_name.lower():
                filename = config.get("filename")
                if filename:
                    image_path = self.maps_dir / filename
                    if image_path.exists():
                        return str(image_path)
                        
        # Return placeholder if enabled
        if self.maps_config.get("placeholders", {}).get("enabled", False):
            placeholder_filename = self.maps_config["placeholders"]["default_image"]
            placeholder_path = self.maps_dir / placeholder_filename
            if placeholder_path.exists():
                return str(placeholder_path)
                
        self.logger.error("No image found for map: %s", map_name)
        return None
        
    def get_map_info(self, map_name):
        """Get detailed information about a map"""
        maps = self.maps_config.get("maps", {})
        return maps.get(map_name, {})
        
    def add_map(self, map_name, filename, realm=None, official_name=None):
        """Add a new map to the configuration"""
        maps = self.maps_config.setdefault("maps", {})
        maps[map_name] = {
            "filename": filename,
            "realm": realm or map_name,
            "official_name": official_name or map_name
        }
        self.save_maps_config(self.maps_config)
        self.logger.info("Added new map: %s", map_name)
        
    def remove_map(self, map_name):
        """Remove a map from the configuration"""
        maps = self.maps_config.get("maps", {})
        if map_name in maps:
            del maps[map_name]
            self.save_maps_config(self.maps_config)
            self.logger.info("Removed map: %s", map_name)
            return True
        return False
        
    def create_placeholder_image(self):
        """Create a placeholder image for missing maps"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create placeholder image
            width, height = 800, 600
            image = Image.new('RGB', (width, height), color='#2C2C2C')
            draw = ImageDraw.Draw(image)
            
            # Try to use a font, fallback to default
            try:
                font = ImageFont.truetype("arial.ttf", 48)
                small_font = ImageFont.truetype("arial.ttf", 24)
            except OSError:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Draw text
            text = "MAP IMAGE"
            subtext = "Place map images in /maps/ folder"
            
            # Center the text
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (width - text_width) // 2
            text_y = (height - text_height) // 2 - 50
            
            bbox_sub = draw.textbbox((0, 0), subtext, font=small_font)
            subtext_width = bbox_sub[2] - bbox_sub[0]
            subtext_x = (width - subtext_width) // 2
            subtext_y = text_y + text_height + 20
            
            draw.text((text_x, text_y), text, fill='white', font=font)
            draw.text((subtext_x, subtext_y), subtext, fill='#CCCCCC', font=small_font)
            
            # Save placeholder
            placeholder_path = self.maps_dir / "placeholder_map.jpg"
            image.save(placeholder_path)
            self.logger.info("Created placeholder image: %s", placeholder_path)
            
        except ImportError:
            self.logger.warning("PIL not available, cannot create placeholder image")
        except Exception as e:
            self.logger.error("Error creating placeholder image: %s", e)
