# Copilot Instructions for DbD Communication App

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->
<!-- Este archivo es utilizado para darle contexto a Copilot! Para más informacion del porque de este archivo, visita https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->
<!-- Copilot se emplea como herramienta de asistencia. Todo el código generado es evaluado, editado y adaptado por mí según los requerimientos del proyecto y
espero que todos los que contribuyan y ocupen esta valiosa herramienta, en este proyecto sea SOLO COMO ASISTENCIA. -->
## Project Context
This is a Python application for Dead by Daylight (DbD) that provides external map detection and communication assistance. The application:

- Uses OCR to detect map names from screenshots
- Displays map images with sector overlays (12-hour clock or 9-zone numpad style)
- Provides click and keyboard interaction for callouts
- Includes text-to-speech functionality
- Must remain completely external to the game (no memory injection or overlays)

## Key Requirements
- 100% external application - no game memory access
- OCR-based map detection using pytesseract
- GUI with tkinter or PyQt5
- Local map image storage
- JSON configuration for map mapping
- Keyboard shortcuts and click interactions
- Optional text-to-speech for callouts

## Security Note (IMPORTANT)
This application must never interact directly with the game's memory or inject any code to avoid account bans.
