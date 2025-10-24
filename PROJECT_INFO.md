# 📋 Información del Proyecto - Scripts CLI

## 🏗️ Estructura del Proyecto

```
scripts/
├── main.py              # Aplicación CLI principal con Typer
├── gui.py               # Interfaz gráfica con tkinter
├── demo.py              # Script de demostración
├── setup.sh             # Script de instalación automática
├── pyproject.toml       # Configuración y gestión de dependencias
├── README.md            # Documentación completa
├── PROJECT_INFO.md      # Este archivo (información técnica)
├── .python-version      # Versión de Python (3.13)
├── .venv/               # Entorno virtual de Python
├── .git/                # Control de versiones Git
├── .gitignore           # Archivos ignorados por Git
├── .vscode/             # Configuración del IDE
│   └── settings.json
└── .windsurfrules       # Reglas y preferencias del usuario
```

## 🛠️ Tecnologías Elegidas

### **CLI Framework**
- **Typer** (>=0.9.0) - Framework moderno para CLI en Python
  - Características: Type hints, validación automática, ayuda generada
  - Instalación: `typer[all]` (incluye todas las funcionalidades)

### **GUI Framework**
- **tkinter** - Interfaz gráfica nativa de Python
  - Ventajas: Incluido en Python, multiplataforma, ligero
  - Componentes usados: Frame, Label, Entry, Button, ScrolledText

### **Gestión de Dependencias**
- **pyproject.toml** - Estándar moderno de Python (PEP 518)
- **uv** - Gestor de paquetes ultrarrápido de Astral
  - Entorno virtual: .venv (gestionado por uv)
  - Python requerido: >=3.13
  - Instalación: https://docs.astral.sh/uv/

### **Estructura de Código**
- **Arquitectura modular**: CLI y GUI separados pero integrados
- **Patrón Command**: Cada comando CLI es una función decorada
- **Ejecución asíncrona**: GUI usa threading para no bloquear interfaz

## 🎯 Comandos CLI Implementados

### `hello [NOMBRE]`
- **Propósito**: Saluda a una persona con mensaje personalizado
- **Argumentos**: 
  - `name` (requerido): Nombre de la persona
- **Opciones**:
  - `--greeting, -g`: Saludo personalizado (default: "Hola")
- **Ejemplo**: `python main.py hello "María" --greeting "Buenos días"`

### `info`
- **Propósito**: Muestra información sobre la aplicación
- **Sin parámetros**
- **Salida**: Versión, descripción, características

### `gui`
- **Propósito**: Lanza la interfaz gráfica tkinter
- **Sin parámetros**
- **Funcionalidad**: Abre ventana GUI con controles interactivos

## 🖥️ Características de la GUI

### **Componentes Principales**
1. **Formulario Hello**: Campos para nombre y saludo personalizado
2. **Botones Rápidos**: Info, Ayuda, Limpiar output
3. **Área de Salida**: ScrolledText para mostrar resultados
4. **Barra de Estado**: Información en tiempo real

### **Funcionalidades Técnicas**
- **Threading**: Ejecución asíncrona de comandos CLI
- **Subprocess**: Integración con comandos del sistema
- **Validación**: Campos requeridos y mensajes de error
- **UX**: Interfaz responsive y moderna

## 🔧 Configuración del Entorno

### **Instalación Automática con uv**
```bash
./setup.sh  # Verifica uv, crea .venv, sincroniza dependencias
```

### **Instalación Manual con uv**
```bash
# Crear entorno virtual
uv venv

# Instalar dependencias
uv sync
```

### **Uso con uv**
```bash
# Ejecutar directamente con uv (recomendado)
uv run python main.py --help
uv run python main.py hello "Usuario"
uv run python main.py gui

# O activar entorno manualmente
source .venv/bin/activate
python main.py --help
```

## 📦 Dependencias

### **Principales**
- `typer[all]>=0.9.0` - Framework CLI completo
  - Incluye: rich (output), click (core), shellingham (shell detection)

### **Estándar (incluidas en Python)**
- `tkinter` - GUI framework
- `subprocess` - Ejecución de comandos
- `threading` - Concurrencia
- `pathlib` - Manejo de rutas

## 🎨 Decisiones de Diseño

### **CLI con Typer**
- **Ventajas**: Type safety, documentación automática, validación
- **Patrón**: Decoradores para comandos, argumentos tipados
- **Extensibilidad**: Fácil añadir nuevos comandos

### **GUI con tkinter**
- **Ventajas**: Nativo, sin dependencias externas, multiplataforma
- **Patrón**: Clase principal con métodos para cada funcionalidad
- **Integración**: Ejecuta comandos CLI via subprocess

### **Arquitectura**
- **Separación de responsabilidades**: CLI y GUI independientes
- **Reutilización**: GUI reutiliza lógica CLI
- **Mantenibilidad**: Código modular y bien documentado

## 🚀 Extensiones Futuras

### **CLI**
- Más comandos (archivos, red, sistema)
- Configuración persistente
- Plugins/extensiones

### **GUI**
- Más formularios para otros comandos
- Configuración visual
- Temas y personalización

### **Integración**
- Base de datos para configuración
- API REST para funcionalidades remotas
- Empaquetado como ejecutable (.app, .exe)
