# Guía de Instalación - DbD Communication App

## Requisitos del Sistema

### Software Necesario
- **Python 3.8+** (recomendado Python 3.9 o superior)
- **Tesseract OCR** para detección de mapas
- **Windows 10/11** (otras plataformas no han sido probadas)

### Hardware Mínimo
- **RAM:** 4GB (recomendado 8GB)
- **Procesador:** Dual-core 2.5GHz o superior
- **Resolución:** 1920x1080 (configuración optimizada para esta resolución)

## Instalación Paso a Paso

### 1. Instalar Python
1. Descarga Python desde [python.org](https://www.python.org/downloads/)
2. **IMPORTANTE:** Durante la instalación, marca "Add Python to PATH"
3. Verifica la instalación abriendo una terminal y ejecutando:
   ```cmd
   python --version
   ```

### 2. Instalar Tesseract OCR
1. Descarga Tesseract desde [GitHub Releases](https://github.com/UB-Mannheim/tesseract/wiki)
2. Instala en la ruta por defecto: `C:\Program Files\Tesseract-OCR\`
3. Si instalas en otra ubicación, actualiza `config/ocr_config.json`

### 3. Clonar o Descargar el Proyecto
```bash
git clone https://github.com/tu-usuario/DbDCom.git
cd DbDCom
```

### 4. Crear Entorno Virtual (Recomendado)
```cmd
python -m venv dbd_env
dbd_env\Scripts\activate
```

### 5. Instalar Dependencias
```cmd
pip install -r requirements.txt
```

### 6. Ejecutar la Aplicación
```cmd
python main.py
```

## Configuración Inicial

La aplicación viene preconfigurada y lista para usar. Los archivos de configuración incluyen:

- `config/ocr_config.json` - Configuración de Tesseract OCR
- `config/maps_config.json` - Mapas disponibles
- `maps/` - Imágenes de mapas de ejemplo

## Solución de Problemas

### Error: "tesseract is not installed"
- Verifica que Tesseract esté instalado en `C:\Program Files\Tesseract-OCR\`
- Actualiza la ruta en `config/ocr_config.json`

### Error: "No module named 'tkinter'"
- Reinstala Python asegurándote de incluir tkinter

### La aplicación no detecta mapas
1. Verifica que Dead by Daylight esté en modo ventana
2. Ajusta las coordenadas de captura en `config/ocr_config.json`
```

## Paso 5: Ejecutar

```bash
python main.py
```
