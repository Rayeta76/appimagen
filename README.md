# AppImagen

Aplicación de escritorio para etiquetar imágenes usando PySide6 y un checkpoint local de Florence 2.

## Requisitos
- Python 3.11
- PySide6
- Pillow

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

## Empaquetado
1. Ejecuta `build.bat` para generar el ejecutable con PyInstaller.
2. Con la herramienta **Advanced Installer** (o alternativa gratuita como WiX Toolset) crea un proyecto MSI e incluye el EXE generado en `dist/main.exe`.
3. Sigue el asistente de tu herramienta para producir el instalador.
