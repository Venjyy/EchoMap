# Contribuir al Proyecto

> ⚠️ **Proyecto en Desarrollo** - Actualmente en fase inicial

## 🚧 Estado del Proyecto

Este proyecto está en desarrollo inicial. Los componentes principales están siendo desarrollados y la funcionalidad no está completa.

## 🎯 Áreas de Contribución

### Inmediatas (cuando esté listo):
- [ ] Optimización del OCR
- [ ] Mejora de la interfaz gráfica
- [ ] Testing y validación
- [ ] Documentación

### Futuras:
- [ ] Soporte para más resoluciones
- [ ] Mejoras de rendimiento
- [ ] Integración con OBS
- [ ] Soporte multiplataforma

## 🔧 Configuración para Desarrollo

```bash
# Clonar repositorio
git clone <repo-url>
cd DbDCom

# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows

# Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install pytest black flake8

# Ejecutar tests (cuando estén disponibles)
pytest

# Formatear código
black src/
```

## 📋 Estándares de Código

- **Formato**: Black
- **Linting**: Flake8  
- **Docstrings**: Google style
- **Tests**: pytest

## 🤝 Proceso de Contribución

1. Fork del repositorio
2. Crear branch de feature (`git checkout -b feature/nueva-feature`)
3. Desarrollar y testear cambios
4. Seguir estándares de código
5. Commit con mensaje descriptivo
6. Push y crear Pull Request

## ⚠️ Notas Importantes

- **Seguridad**: Nunca implementar funciones que accedan a memoria del juego
- **External Only**: Todas las funciones deben ser externas al juego
- **No Ban Risk**: Mantener compatibilidad con ToS de DbD

## 📞 Contacto

Para dudas sobre contribuciones, crear un Issue en GitHub.
