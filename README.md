# VITALINUX - Verificación de Equipos

Aplicación de escritorio para verificar el estado de equipos de trabajo.

## Ejecutar la aplicación

```bash
uv run python vitalinux_equipment_check.py
```

## Características

- ✅ Interfaz moderna con ttkbootstrap
- ✅ Scroll suave por píxeles
- ✅ Radiobuttons personalizados blancos inicialmente
- ✅ Validación inteligente de formularios
- ✅ Exportación a JSON con metadatos completos
- ✅ Campos obligatorios: Pantalla y Teclado
- ✅ Campos opcionales: Ratón, Batería, Otros

## Dependencias

- Python 3.11+
- ttkbootstrap
- tkinter (incluido con Python)

## Crear Ejecutable Linux

### Construcción Automática
```bash
# Crear ejecutable para Linux
python build_executable.py

# O usando uv directamente
uv run python build_executable.py
```

### Construcción Manual con PyInstaller
```bash
# Construcción básica
uv run pyinstaller --onefile --windowed vitalinux_equipment_check.py
```

### Crear Paquete DEB
```bash
./create_deb.sh  # Crea un paquete .deb para instalación
```

## Archivos generados

La aplicación genera archivos JSON con el formato:
`vitalinux_verificacion_equipos_YYYYMMDD_HHMMSS.json`
