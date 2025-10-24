#!/usr/bin/env python3
"""
Launcher para VITALINUX - Verificación de Equipos
Optimizado para pantalla completa con texto grande
"""

import sys
import os

def main():
    print("🏢 VITALINUX - Verificación de Equipos")
    print("📺 Iniciando en modo pantalla completa...")
    print("🔤 Texto optimizado para mejor legibilidad")
    print("=" * 60)
    
    try:
        from equipment_check_styled import main as run_app
        run_app()
    except ImportError as e:
        print(f"❌ Error al importar la aplicación: {e}")
        print("💡 Asegúrate de que equipment_check_styled.py esté en el directorio actual")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
