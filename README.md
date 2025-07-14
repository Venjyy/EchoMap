# DbD Communication App

Una aplicación externa completamente segura para Dead by Daylight que detecta mapas automáticamente mediante OCR y proporciona un sistema de comunicación por sectores para facilitar los "callouts" durante las partidas.

## ⚠️ Seguridad

Esta aplicación es **100% externa** al juego y **NO** interactúa con la memoria del juego, no inyecta código, ni usa overlays dentro del ejecutable de DbD. Es completamente segura y no puede causar baneos.

## 🎯 Características

- **Detección automática de mapas** mediante OCR (Tesseract)
- **Interfaz gráfica** con overlays de sectores
- **Dos modos de sectores**: Reloj de 12 horas o Teclado numérico de 9 zonas
- **Interacción múltiple**: Clics del mouse o atajos de teclado
- **Text-to-Speech** opcional para callouts audibles
- **Feedback visual**: Sectores seleccionados se resaltan en rojo
- **Configuración JSON** para personalización
- **Sistema de logs** para debugging

## 📋 Requisitos del Sistema

- **Python 3.8+**
- **Windows 10/11** (recomendado)
- **Tesseract OCR** instalado
- **Micrófono/Altavoces** para TTS (opcional)

## 🚀 Instalación

### 1. Clonar o descargar el proyecto
```bash
git clone https://github.com/Venjyy/EchoMap.git
cd EchoMap
```

### 2. Instalar Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Instalar Tesseract OCR

**Windows:**
- Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
- Instalar en la ubicación por defecto: `C:\\Program Files\\Tesseract-OCR\\`
- Agregar al PATH del sistema

**Verificar instalación:**
```bash
tesseract --version
```

### 4. Configurar las imágenes de mapas

Coloca las imágenes de los mapas de DbD en la carpeta `maps/`:
```
maps/
├── haddonfield.jpg
├── springwood.jpg
├── macmillan.jpg
├── autohaven.jpg
└── ...
```

**Formatos soportados:** JPG, PNG, BMP
**Resolución recomendada:** 800x600 píxeles

## 🎮 Uso

### Iniciar la aplicación
```bash
python main.py
```

### Flujo de trabajo básico:

1. **Modo automático:**
   - Hacer clic en "Start Detection"
   - Jugar DbD normalmente
   - La app detectará automáticamente el mapa al inicio de la partida

2. **Modo manual:**
   - Seleccionar mapa del dropdown
   - Hacer clic en "Load Map"

3. **Hacer callouts:**
   - **Mouse:** Hacer clic en los sectores del mapa
   - **Teclado:** 
     - Modo reloj: F1-F12
     - Modo numpad: 1-9
   - **Feedback visual:** El sector seleccionado se resalta en rojo

### Ejemplo de uso:
- Clic en sector 3 → Se resalta en rojo + "Sector 3" (TTS si está activo)
- Tecla F9 → Se resalta en rojo + "Sector 9" (TTS si está activo)
