#!/usr/bin/env python3
"""
Launcher para la aplicación Migas de verificación de equipos
Versión estilizada con paleta de colores corporativa
"""

import sys
import os

def main():
    print("🏢 Iniciando aplicación MIGAS...")
    print("📋 Sistema de Verificación de Equipos")
    print("🎨 Versión estilizada con paleta corporativa")
    print("-" * 50)
    
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
