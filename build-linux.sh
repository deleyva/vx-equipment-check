#!/bin/bash

# Script para construir Comprobación de PC Vitalinux en Linux
# Ejecutar este script en una máquina Ubuntu/VitaLinux

set -e

echo "🚀 Construyendo Comprobación de PC Vitalinux para Linux..."

# Verificar que estamos en Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Este script debe ejecutarse en Linux"
    echo "💡 Para construir desde macOS, usa: npm run build"
    exit 1
fi

# Instalar dependencias del sistema si no existen
echo "📦 Verificando dependencias del sistema..."
if ! dpkg -l | grep -q libwebkit2gtk-4.0-dev; then
    echo "🔧 Instalando dependencias..."
    sudo apt update
    sudo apt install -y \
        libwebkit2gtk-4.0-dev \
        build-essential \
        curl \
        wget \
        libssl-dev \
        libgtk-3-dev \
        libayatana-appindicator3-dev \
        librsvg2-dev
fi

# Verificar Rust
if ! command -v cargo &> /dev/null; then
    echo "🦀 Instalando Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source ~/.cargo/env
fi

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo "📗 Instalando Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt install -y nodejs
fi

# Instalar dependencias del proyecto
echo "📦 Instalando dependencias del proyecto..."
npm install

# Construir la aplicación
echo "🏗️ Construyendo aplicación..."
npm run build

# Mostrar resultados
echo ""
echo "✅ ¡Construcción completada!"
echo ""
echo "📁 Archivos generados en:"
echo "   src-tauri/target/release/bundle/"
echo ""

if [ -f "src-tauri/target/release/bundle/deb/"*.deb ]; then
    echo "📦 Paquete .deb:"
    ls -la src-tauri/target/release/bundle/deb/*.deb
fi

if [ -f "src-tauri/target/release/bundle/appimage/"*.AppImage ]; then
    echo "📱 AppImage:"
    ls -la src-tauri/target/release/bundle/appimage/*.AppImage
fi

if [ -f "src-tauri/target/release/bundle/rpm/"*.rpm ]; then
    echo "📦 Paquete .rpm:"
    ls -la src-tauri/target/release/bundle/rpm/*.rpm
fi

echo ""
echo "🎯 Para instalar en VitaLinux:"
echo "   sudo dpkg -i src-tauri/target/release/bundle/deb/*.deb"
echo "   sudo apt install -f  # Si hay dependencias faltantes"
echo ""
echo "🚀 ¡Listo para distribución!"
