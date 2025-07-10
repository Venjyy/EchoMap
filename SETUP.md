# Configuración Inicial

## Paso 1: Copiar archivos de configuración

```bash
# Copiar templates a archivos de configuración
copy config\ocr_config.json.template config\ocr_config.json
copy config\maps_config.json.template config\maps_config.json
```

## Paso 2: Configurar Tesseract OCR

1. Instalar Tesseract desde: https://github.com/UB-Mannheim/tesseract/wiki
2. Editar `config/ocr_config.json` y configurar:
   ```json
   {
     "tesseract_path": "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
   }
   ```

## Paso 3: Agregar imágenes de mapas

1. Crear directorio `maps/` si no existe
2. Agregar imágenes de mapas (.jpg, .png, .bmp)
3. Configurar nombres en `config/maps_config.json`

## Paso 4: Instalar dependencias

```bash
pip install -r requirements.txt
```

## Paso 5: Ejecutar

```bash
python main.py
```
