#!/bin/bash
# Script para crear paquete DEB para Linux
APP_NAME="vitalinux-equipment-check"
VERSION="1.0.0"

echo "🐧 Creando paquete DEB para Linux..."

# Crear estructura del paquete
mkdir -p "deb_package/DEBIAN"
mkdir -p "deb_package/usr/bin"
mkdir -p "deb_package/usr/share/applications"

# Copiar ejecutable
cp "dist/VitalinuxEquipmentCheck" "deb_package/usr/bin/"

# Crear archivo de control
cat > "deb_package/DEBIAN/control" << EOF
Package: $APP_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: amd64
Maintainer: VITALINUX <info@vitalinux.com>
Description: Aplicación para verificación de equipos
 Aplicación de escritorio para verificar el estado de equipos de trabajo.
EOF

# Crear archivo .desktop
cat > "deb_package/usr/share/applications/$APP_NAME.desktop" << EOF
[Desktop Entry]
Name=VITALINUX Equipment Check
Comment=Verificación de equipos
Exec=/usr/bin/VitalinuxEquipmentCheck
Terminal=false
Type=Application
Categories=Utility;
EOF

# Construir el paquete
dpkg-deb --build deb_package "dist/$APP_NAME-$VERSION.deb"

# Limpiar
rm -rf deb_package

echo "✅ Paquete DEB creado: dist/$APP_NAME-$VERSION.deb"
