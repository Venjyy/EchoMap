# DbD Communication App (WIP)

> ⚠️ **Work in Progress** - Este proyecto está en desarrollo inicial

Una aplicación externa para Dead by Daylight que proporciona un sistema de comunicación por sectores para facilitar los "callouts" durante las partidas.

## 🎯 Objetivo del Proyecto

Crear una herramienta **100% externa y segura** que permita:
- Detección automática de mapas mediante OCR
- Visualización de mapas con sectores numerados
- Sistema de callouts rápidos por sectores
- Compatibilidad con atajos de teclado y clicks

## ⚠️ Seguridad

Esta aplicación será **completamente externa** al juego:
- ❌ Sin acceso a memoria del juego
- ❌ Sin inyección de código
- ❌ Sin overlays dentro del ejecutable
- ✅ Solo capturas de pantalla externas

## 🚧 Estado Actual

**Implementado:**
- [x] Estructura base del proyecto
- [x] Sistema de configuración JSON
- [x] Interfaz gráfica básica
- [x] Gestión de mapas placeholder

**En Desarrollo:**
- [ ] Integración OCR completa
- [ ] Optimización de detección
- [ ] Sistema TTS
- [ ] Mapas reales de DbD

**Planeado:**
- [ ] Compilación a ejecutable
- [ ] Documentación completa
- [ ] Testing exhaustivo

## 📋 Requisitos Planeados

- Python 3.8+
- Tesseract OCR
- Windows 10/11

## 📁 Estructura del Proyecto

```
DbDCom/
├── src/                   # Código fuente principal
│   ├── dbd_app.py        # Aplicación principal
│   ├── ocr_detector.py   # Detector OCR (WIP)
│   ├── map_manager.py    # Gestor de mapas
│   ├── gui_interface.py  # Interfaz gráfica
│   └── tts_handler.py    # Text-to-Speech (WIP)
├── config/               # Configuraciones (templates)
├── maps/                 # Directorio para imágenes de mapas
├── main.py              # Punto de entrada
├── setup.py             # Script de instalación
├── demo.py              # Script de demostración
└── requirements.txt     # Dependencias Python
```

## 🎮 Concepto de Uso

1. **Detección automática**: La app detectará el mapa al inicio de partida
2. **Visualización de sectores**: Overlay con sectores numerados (reloj/numpad)
3. **Callouts rápidos**: Click o tecla → "Killer en sector 3"
4. **External safe**: Sin riesgo de ban, completamente externa

## 🔧 Configuración Inicial (Cuando esté completo)

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar Tesseract OCR
# Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki

# Ejecutar aplicación
python main.py
```

## 🎨 Modos de Sectores Planeados

### Modo Reloj (12 sectores)
- F1-F12 para cada hora del reloj
- Sector 12 = arriba, crecimiento horario

### Modo Numpad (9 sectores)  
- 1-9 siguiendo layout numérico
- 7-8-9 (arriba), 4-5-6 (medio), 1-2-3 (abajo)

## 🤝 Contribuciones

El proyecto está en desarrollo inicial. Las contribuciones serán bienvenidas cuando esté más estable.

## 📄 Licencia

MIT License (pendiente de archivo LICENSE)

## ⚠️ Disclaimer

- Proyecto no oficial, no afiliado con Behaviour Interactive Inc.
- Dead by Daylight es marca registrada de Behaviour Interactive Inc.
- **Trabajo en progreso** - No apto para uso en producción aún
