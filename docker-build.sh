#!/bin/bash

# Script para construir VITALINUX Equipment Check usando Docker
# Esto garantiza un entorno de build consistente

set -e

echo "🐳 Construyendo VITALINUX Equipment Check con Docker..."

# Construir la imagen Docker
echo "🐳 Construyendo imagen Docker para AMD64..."
docker build --platform linux/amd64 -t vitalinux-equipment-check-builder .

# Crear contenedor y extraer archivos
echo "🏗️ Ejecutando build en contenedor..."
docker run --platform linux/amd64 --name vx-build-temp vitalinux-equipment-check-builder

# Crear directorio de salida
mkdir -p ./docker-output

# Copiar archivos del contenedor
echo "📁 Extrayendo archivos construidos..."
docker cp vx-build-temp:/output/. ./docker-output/

# Limpiar contenedor temporal
docker rm vx-build-temp

echo ""
echo "✅ ¡Build completado!"
echo ""
echo "📦 Archivos generados en ./docker-output/:"
ls -la ./docker-output/

if [ -d "./docker-output/deb" ]; then
    echo ""
    echo "🐧 Paquete .deb para VitaLinux/Ubuntu:"
    ls -la ./docker-output/deb/
fi

if [ -d "./docker-output/appimage" ]; then
    echo ""
    echo "📱 AppImage portable:"
    ls -la ./docker-output/appimage/
fi

if [ -d "./docker-output/rpm" ]; then
    echo ""
    echo "📦 Paquete .rpm para Fedora/CentOS:"
    ls -la ./docker-output/rpm/
fi

echo ""
echo "🚀 Para instalar en VitaLinux:"
echo "   sudo dpkg -i ./docker-output/deb/*.deb"
echo "   sudo apt install -f"
echo ""
echo "📱 Para usar AppImage:"
echo "   chmod +x ./docker-output/appimage/*.AppImage"
echo "   ./docker-output/appimage/*.AppImage"
