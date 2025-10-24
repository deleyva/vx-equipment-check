#!/usr/bin/env python3
"""
Script para crear ejecutable de Linux para VITALINUX Equipment Check
"""

import os
import sys
import subprocess

def build_executable():
    """Construye el ejecutable para Linux usando PyInstaller"""
    
    print("🐧 Construyendo ejecutable para Linux...")
    
    # Configuración de PyInstaller
    app_name = "VitalinuxEquipmentCheck"
    main_script = "vitalinux_equipment_check.py"
    
    # Argumentos de PyInstaller para Linux
    pyinstaller_args = [
        "uv", "run", "pyinstaller",
        "--onefile",                    # Un solo archivo ejecutable
        "--windowed",                   # Sin consola (GUI)
        "--name", app_name,
        "--clean",                      # Limpiar cache antes de construir
        "--noconfirm",                  # No pedir confirmación
        "--distpath=dist",              # Directorio de salida
        "--workpath=build",             # Directorio de trabajo
        main_script
    ]
    
    try:
        # Ejecutar PyInstaller
        print(f"📦 Ejecutando: {' '.join(pyinstaller_args)}")
        result = subprocess.run(pyinstaller_args, check=True, capture_output=True, text=True)
        
        print("✅ Ejecutable creado exitosamente!")
        print(f"📁 Ubicación: dist/{app_name}")
        
        # Mostrar información del archivo generado
        exe_path = f"dist/{app_name}"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"📊 Tamaño: {size_mb:.1f} MB")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al crear el ejecutable:")
        print(f"   Salida: {e.stdout}")
        print(f"   Error: {e.stderr}")
        return False
    
    return True

def create_deb_installer():
    """Crea script para crear paquete DEB de Linux"""
    
    deb_script = """#!/bin/bash
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
"""
    
    with open("create_deb.sh", "w") as f:
        f.write(deb_script)
    os.chmod("create_deb.sh", 0o755)

def main():
    """Función principal"""
    print("🚀 VITALINUX Equipment Check - Constructor de Ejecutable Linux")
    print("=" * 60)
    
    # Verificar que existe el archivo principal
    if not os.path.exists("vitalinux_equipment_check.py"):
        print("❌ Error: No se encuentra vitalinux_equipment_check.py")
        return 1
    
    # Crear directorios de salida
    os.makedirs("dist", exist_ok=True)
    os.makedirs("build", exist_ok=True)
    
    # Construir ejecutable
    if build_executable():
        print("\n🎉 ¡Ejecutable creado exitosamente!")
        
        # Crear script de instalación DEB
        create_deb_installer()
        print("📋 Script de instalación DEB creado")
        
        print("\n📖 Instrucciones:")
        print("   • Ejecuta: ./create_deb.sh para crear un paquete DEB")
        print("📁 Ejecutable disponible en: dist/VitalinuxEquipmentCheck")
        
        return 0
    else:
        print("❌ Error al crear el ejecutable")
        return 1

if __name__ == "__main__":
    sys.exit(main())
