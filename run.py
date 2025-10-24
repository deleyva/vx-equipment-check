#!/usr/bin/env python3
"""
Script de lanzamiento para VITALINUX Equipment Check
"""

import subprocess
import sys
import os

def main():
    """Lanza la aplicación VITALINUX"""
    try:
        # Cambiar al directorio del script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Ejecutar la aplicación
        subprocess.run([sys.executable, "vitalinux_equipment_check.py"], check=True)
        
    except KeyboardInterrupt:
        print("\n✅ Aplicación cerrada por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar la aplicación: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
