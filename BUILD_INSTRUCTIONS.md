# Instrucciones para compilar a EXE

Para crear un ejecutable standalone de la aplicación DbD Communication App:

## Requisitos
- PyInstaller instalado: `pip install pyinstaller`
- Todas las dependencias instaladas
- Tesseract OCR en el sistema

## Comando de compilación

```bash
pyinstaller --onefile --windowed --name "DbDCommunicationApp" --icon=icon.ico --add-data "config;config" --add-data "maps;maps" --hidden-import=pytesseract --hidden-import=pyttsx3 --hidden-import=keyboard main.py
```

## Explicación de parámetros:

- `--onefile`: Crear un solo archivo ejecutable
- `--windowed`: Sin ventana de consola (GUI)
- `--name`: Nombre del ejecutable
- `--icon`: Ícono del ejecutable (opcional)
- `--add-data`: Incluir directorios en el ejecutable
- `--hidden-import`: Forzar inclusión de módulos

## Estructura del ejecutable:

```
dist/
└── DbDCommunicationApp.exe
```

## Distribución:

El ejecutable generado incluye:
- Python runtime
- Todas las librerías necesarias
- Archivos de configuración
- Mapas de ejemplo

**Nota:** El usuario final aún necesita Tesseract OCR instalado en su sistema.
