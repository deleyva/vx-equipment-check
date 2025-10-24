#!/bin/bash

# Script de configuración para Scripts CLI con uv
echo "🚀 Configurando Scripts CLI con uv..."

# Verificar que uv está instalado
if ! command -v uv &> /dev/null; then
    echo "❌ Error: uv no está instalado"
    echo "📥 Instala uv desde: https://docs.astral.sh/uv/getting-started/installation/"
    echo "💡 Comando rápido: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Verificar si ya existe el entorno virtual
if [ ! -d ".venv" ]; then
    echo "📦 Creando entorno virtual con uv..."
    uv venv
else
    echo "📦 Usando entorno virtual existente..."
fi

# Sincronizar dependencias con uv
echo "📥 Instalando dependencias con uv..."
uv sync

echo "✅ ¡Configuración completada con uv!"
echo ""
echo "Para usar la aplicación:"
echo "1. Activa el entorno virtual: source .venv/bin/activate"
echo "   O usa uv directamente: uv run python main.py"
echo "2. Ejecuta la CLI: uv run python main.py --help"
echo "3. Lanza la GUI: uv run python main.py gui"
echo ""
echo "🎯 Comandos útiles con uv:"
echo "• uv add [paquete]     - Añadir dependencia"
echo "• uv remove [paquete]  - Eliminar dependencia"
echo "• uv run [comando]     - Ejecutar en el entorno"
echo "• uv sync              - Sincronizar dependencias"
echo ""
echo "¡Disfruta usando Scripts CLI con uv! 🎉"
