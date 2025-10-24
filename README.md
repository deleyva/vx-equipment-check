# 🚀 Scripts CLI

Una aplicación CLI potente desarrollada con **Typer** que incluye una interfaz gráfica opcional con **tkinter**.

## 📋 Características

- ✅ **CLI moderna** con Typer
- 🖥️ **Interfaz gráfica** opcional con tkinter
- 🎨 **Comandos interactivos** y fáciles de usar
- 📦 **Gestión de dependencias** con pyproject.toml
- 🐍 **Compatible con Python 3.13+**

## 🛠️ Instalación

### Con uv (Recomendado)

1. **Instala uv** si no lo tienes:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clona o descarga** el proyecto

3. **Configura el entorno**:
   ```bash
   ./setup.sh
   ```

### Instalación Manual con uv

```bash
# Crear entorno virtual
uv venv

# Instalar dependencias
uv sync
```

## 🚀 Uso

### Línea de Comandos (CLI)

#### Ayuda general
```bash
# Con uv (recomendado)
uv run python main.py --help

# O activando el entorno
source .venv/bin/activate
python main.py --help
```

#### Comando Hello
```bash
# Saludo básico
uv run python main.py hello "Tu Nombre"

# Saludo personalizado
uv run python main.py hello "Tu Nombre" --greeting "Buenos días"
uv run python main.py hello "Tu Nombre" -g "¡Hola"
```

#### Información de la aplicación
```bash
uv run python main.py info
```

#### Lanzar interfaz gráfica
```bash
uv run python main.py gui
```

### Interfaz Gráfica (GUI)

La interfaz gráfica proporciona:

- **📝 Formulario interactivo** para el comando hello
- **🔘 Botones rápidos** para comandos comunes
- **📺 Área de salida** para ver resultados
- **📊 Barra de estado** con información en tiempo real

Para lanzar la GUI:
```bash
uv run python main.py gui
```

O ejecutar directamente:
```bash
uv run python gui.py
```

## 📁 Estructura del Proyecto

```
scripts/
├── main.py          # Aplicación CLI principal con Typer
├── gui.py           # Interfaz gráfica con tkinter
├── pyproject.toml   # Configuración y dependencias
├── README.md        # Este archivo
└── .python-version  # Versión de Python
```

## 🔧 Desarrollo

### Añadir nuevos comandos CLI

1. **Añade una nueva función** en `main.py`:
   ```python
   @app.command()
   def mi_comando(parametro: str):
       """Descripción del comando"""
       typer.echo(f"Ejecutando: {parametro}")
   ```

2. **Úsalo desde CLI**:
   ```bash
   python main.py mi-comando "valor"
   ```

### Extender la GUI

1. **Modifica** `gui.py` para añadir nuevos widgets
2. **Conecta** los widgets con los comandos CLI usando `subprocess`

## 🎯 Ejemplos de Uso

### Ejemplo 1: Saludo personalizado
```bash
uv run python main.py hello "María" --greeting "¡Buenos días"
# Salida: ¡Buenos días, María! 👋
```

### Ejemplo 2: Información de la app
```bash
uv run python main.py info
# Salida:
# 🚀 Scripts CLI v0.1.0
# Una aplicación CLI desarrollada con Typer
# Incluye interfaz gráfica opcional con tkinter
```

### Ejemplo 3: Usar la GUI
```bash
uv run python main.py gui
# Abre la interfaz gráfica
```

## 🤝 Contribuir

1. **Fork** el proyecto
2. **Crea** una rama para tu feature
3. **Haz** commit de tus cambios
4. **Envía** un pull request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

---

**¡Disfruta usando Scripts CLI!** 🎉