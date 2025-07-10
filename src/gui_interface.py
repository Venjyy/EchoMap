#!/usr/bin/env python3
"""
GUI Interface for Map Display with Sector Overlays
"""

import tkinter as tk
from tkinter import ttk
import logging
from PIL import Image, ImageTk, ImageDraw, ImageFont
import keyboard
import math


class MapGUI:
    """GUI for displaying maps with clickable sectors"""

    def __init__(self, map_image_path, map_name, sector_mode="clock", tts_handler=None):
        self.logger = logging.getLogger(__name__)
        self.map_image_path = map_image_path
        self.map_name = map_name
        self.sector_mode = sector_mode  # "clock" or "numpad"
        self.tts_handler = tts_handler

        # GUI components
        self.window = None
        self.canvas = None
        self.image_tk = None
        self.sectors = []

        # Visual feedback state
        self.last_selected_sector = None
        self.base_image = None  # Store the base image without selections

        # Settings
        self.canvas_width = 800
        self.canvas_height = 600
        self.sector_alpha = 100  # Transparency for sector overlays

        self.setup_gui()
        self.setup_keyboard_bindings()

    def setup_gui(self):
        """Setup the map display GUI"""
        self.window = tk.Toplevel()
        self.window.title(f"DbD Map: {self.map_name}")
        self.window.geometry(
            f"{self.canvas_width + 50}x{self.canvas_height + 100}")

        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Title
        title_label = ttk.Label(main_frame, text=f"Map: {self.map_name}",
                                font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 10))

        # Canvas for map image
        self.canvas = tk.Canvas(main_frame, width=self.canvas_width,
                                height=self.canvas_height, bg='black')
        self.canvas.grid(row=1, column=0)

        # Info frame
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=2, column=0, pady=(10, 0), sticky="ew")

        mode_text = "12-Hour Clock" if self.sector_mode == "clock" else "9-Zone Numpad"
        ttk.Label(info_frame, text=f"Mode: {mode_text}").grid(
            row=0, column=0, sticky="w")

        if self.sector_mode == "clock":
            ttk.Label(
                info_frame, text="Keys: F1-F12 or click sectors").grid(row=1, column=0, sticky="w")
        else:
            ttk.Label(
                info_frame, text="Keys: 1-9 or click sectors").grid(row=1, column=0, sticky="w")

        # Last callout display
        self.last_callout_var = tk.StringVar(value="Ready for callouts...")
        ttk.Label(info_frame, textvariable=self.last_callout_var,
                  font=("Arial", 10, "italic")).grid(row=2, column=0, sticky="w")

        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        self.load_and_display_map()

    def load_and_display_map(self):
        """Load map image and create sector overlays"""
        try:
            # Load and resize image
            image = Image.open(self.map_image_path)
            image = image.resize(
                (self.canvas_width, self.canvas_height), Image.Resampling.LANCZOS)

            # Store base image for refreshing
            self.base_image = image.copy()

            # Create overlay with sectors
            overlay_image = self.create_sector_overlay(image)

            # Convert to Tkinter format
            self.image_tk = ImageTk.PhotoImage(overlay_image)

            # Display on canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

            # Bind click events
            self.canvas.bind("<Button-1>", self.on_canvas_click)

            self.logger.info("Map loaded and displayed: %s", self.map_name)

        except Exception as e:
            self.logger.error("Error loading map image: %s", e)
            self.show_error_message()

    def create_sector_overlay(self, base_image, selected_sector=None):
        """Create sector overlay on the map image"""
        # Create a copy for drawing
        overlay = base_image.copy()
        draw = ImageDraw.Draw(overlay, 'RGBA')

        # Try to load font
        try:
            font = ImageFont.truetype("arial.ttf", 24)
            small_font = ImageFont.truetype("arial.ttf", 16)
        except OSError:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()

        if self.sector_mode == "clock":
            self.create_clock_sectors(draw, font, selected_sector)
        else:
            self.create_numpad_sectors(draw, font, selected_sector)

        return overlay

    def create_clock_sectors(self, draw, font, selected_sector=None):
        """Create 12-hour clock style sectors"""
        center_x = self.canvas_width // 2
        center_y = self.canvas_height // 2
        radius = min(center_x, center_y) - 50

        self.sectors = []

        for i in range(12):
            # Calculate angle (12 o'clock = 0 degrees, clockwise)
            angle = (i * 30) - 90  # Start at 12 o'clock
            angle_rad = math.radians(angle)

            # Calculate sector boundaries
            next_angle_rad = math.radians(angle + 30)

            # Create sector points (triangle from center)
            points = [
                center_x, center_y,  # Center point
                center_x + radius *
                math.cos(angle_rad), center_y + radius * math.sin(angle_rad),
                center_x + radius *
                math.cos(next_angle_rad), center_y +
                radius * math.sin(next_angle_rad)
            ]

            # Determine sector color based on selection
            sector_num = 12 if i == 0 else i
            is_selected = selected_sector == sector_num

            if is_selected:
                # Red color for selected sector
                outline_color = 'red'
                # More visible
                fill_color = (255, 0, 0, self.sector_alpha + 50)
                text_fill = 'white'
            else:
                # Default yellow color
                outline_color = 'yellow'
                fill_color = (255, 255, 0, self.sector_alpha)
                text_fill = 'white'

            # Draw sector outline
            draw.polygon(points, outline=outline_color,
                         width=3, fill=fill_color)

            # Calculate text position
            text_angle_rad = math.radians(angle + 15)  # Middle of sector
            text_radius = radius * 0.7
            text_x = center_x + text_radius * math.cos(text_angle_rad)
            text_y = center_y + text_radius * math.sin(text_angle_rad)

            # Draw sector number
            sector_num = 12 if i == 0 else i
            bbox = draw.textbbox((0, 0), str(sector_num), font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            draw.text((text_x - text_width//2, text_y - text_height//2),
                      str(sector_num), fill=text_fill, font=font, stroke_width=1, stroke_fill='black')

            # Store sector info
            self.sectors.append({
                'number': sector_num,
                'points': points,
                'center': (text_x, text_y),
                'hotkey': f'F{sector_num}'
            })

    def create_numpad_sectors(self, draw, font, selected_sector=None):
        """Create 9-zone numpad style sectors"""
        sector_width = self.canvas_width // 3
        sector_height = self.canvas_height // 3

        self.sectors = []

        # Numpad layout (7-8-9 top row, 4-5-6 middle, 1-2-3 bottom)
        numpad_layout = [
            [7, 8, 9],
            [4, 5, 6],
            [1, 2, 3]
        ]

        for row in range(3):
            for col in range(3):
                sector_num = numpad_layout[row][col]

                # Calculate sector boundaries
                x1 = col * sector_width
                y1 = row * sector_height
                x2 = x1 + sector_width
                y2 = y1 + sector_height

                # Determine sector color based on selection
                is_selected = selected_sector == sector_num

                if is_selected:
                    # Red color for selected sector
                    outline_color = 'red'
                    # More visible
                    fill_color = (255, 0, 0, self.sector_alpha + 50)
                    text_fill = 'white'
                else:
                    # Default yellow color
                    outline_color = 'yellow'
                    fill_color = (255, 255, 0, self.sector_alpha)
                    text_fill = 'white'

                # Draw sector outline
                draw.rectangle([x1, y1, x2, y2], outline=outline_color, width=3,
                               fill=fill_color)

                # Calculate text position (center of sector)
                text_x = x1 + sector_width // 2
                text_y = y1 + sector_height // 2

                # Draw sector number
                bbox = draw.textbbox((0, 0), str(sector_num), font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                draw.text((text_x - text_width//2, text_y - text_height//2),
                          str(sector_num), fill=text_fill, font=font, stroke_width=2, stroke_fill='black')

                # Store sector info
                self.sectors.append({
                    'number': sector_num,
                    'bounds': (x1, y1, x2, y2),
                    'center': (text_x, text_y),
                    'hotkey': str(sector_num)
                })

    def on_canvas_click(self, event):
        """Handle mouse clicks on canvas"""
        x, y = event.x, event.y
        clicked_sector = self.get_sector_at_position(x, y)

        if clicked_sector:
            self.make_callout(clicked_sector['number'])

    def get_sector_at_position(self, x, y):
        """Determine which sector was clicked"""
        for sector in self.sectors:
            if self.sector_mode == "clock":
                # For clock sectors, check if point is in triangle
                if self.point_in_triangle(x, y, sector['points']):
                    return sector
            else:
                # For numpad sectors, check if point is in rectangle
                bounds = sector['bounds']
                if bounds[0] <= x <= bounds[2] and bounds[1] <= y <= bounds[3]:
                    return sector
        return None

    def point_in_triangle(self, x, y, triangle_points):
        """Check if point is inside triangle using barycentric coordinates"""
        # Triangle points: [x1, y1, x2, y2, x3, y3]
        x1, y1, x2, y2, x3, y3 = triangle_points

        # Calculate area of triangle
        area = abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

        # Calculate areas of sub-triangles
        area1 = abs((x * (y2 - y3) + x2 * (y3 - y) + x3 * (y - y2)) / 2.0)
        area2 = abs((x1 * (y - y3) + x * (y3 - y1) + x3 * (y1 - y)) / 2.0)
        area3 = abs((x1 * (y2 - y) + x2 * (y - y1) + x * (y1 - y2)) / 2.0)

        # Check if sum of areas equals original area (with small tolerance)
        return abs(area - (area1 + area2 + area3)) < 1

    def setup_keyboard_bindings(self):
        """Setup global keyboard shortcuts"""
        try:
            if self.sector_mode == "clock":
                # F1-F12 for clock mode
                for i in range(1, 13):
                    keyboard.add_hotkey(
                        f'f{i}', lambda sector=i: self.make_callout(sector))
            else:
                # 1-9 for numpad mode
                for i in range(1, 10):
                    keyboard.add_hotkey(
                        f'{i}', lambda sector=i: self.make_callout(sector))

        except Exception as e:
            self.logger.warning("Could not setup global hotkeys: %s", e)

    def make_callout(self, sector_number):
        """Make a callout for the specified sector"""
        try:
            # Update visual feedback first
            self.update_sector_selection(sector_number)

            callout_text = f"Sector {sector_number}"
            self.last_callout_var.set(f"Last callout: {callout_text}")

            # Text-to-speech if available
            if self.tts_handler:
                self.tts_handler.speak(callout_text)

            self.logger.info("Callout made: %s", callout_text)

        except Exception as e:
            self.logger.error("Error making callout: %s", e)

    def show_error_message(self):
        """Show error message when map cannot be loaded"""
        self.canvas.create_text(self.canvas_width//2, self.canvas_height//2,
                                text="Error loading map image\\nCheck logs for details",
                                fill='red', font=("Arial", 16), justify=tk.CENTER)

    def show(self):
        """Show the map window"""
        if self.window:
            self.window.deiconify()
            self.window.lift()
            self.window.focus()

    def close(self):
        """Close the map window"""
        try:
            # Remove keyboard bindings
            keyboard.unhook_all()
        except:
            pass

        if self.window:
            self.window.destroy()
            self.window = None

    def update_sector_selection(self, sector_number):
        """Update visual feedback to show selected sector in red"""
        if self.base_image:
            # Store the selected sector
            self.last_selected_sector = sector_number

            # Recreate the overlay with the selected sector highlighted
            overlay_image = self.create_sector_overlay(
                self.base_image, sector_number)

            # Update the display
            self.image_tk = ImageTk.PhotoImage(overlay_image)
            self.canvas.delete("all")  # Clear previous image
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
