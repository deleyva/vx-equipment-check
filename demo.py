#!/usr/bin/env python3
"""
Demo script para mostrar las funcionalidades de Scripts CLI
sin necesidad de instalar dependencias externas.
"""

def demo_cli():
    """Simula el comportamiento de la CLI"""
    print("🚀 Scripts CLI v0.1.0")
    print("Una aplicación CLI desarrollada con Typer")
    print("Incluye interfaz gráfica opcional con tkinter")
    print()
    
    print("📋 Comandos disponibles:")
    print("  • hello [NOMBRE] - Saluda a una persona")
    print("  • info - Muestra información de la aplicación")
    print("  • gui - Lanza la interfaz gráfica")
    print()
    
    # Simular comando hello
    print("🎯 Ejemplo de comando hello:")
    name = "Usuario"
    greeting = "Hola"
    print(f"$ python main.py hello '{name}' --greeting '{greeting}'")
    print(f"{greeting}, {name}! 👋")
    print()


def demo_gui_info():
    """Muestra información sobre la GUI"""
    print("🖥️ Interfaz Gráfica (GUI):")
    print("  • Formulario interactivo para comandos")
    print("  • Botones rápidos para acciones comunes")
    print("  • Área de salida para ver resultados")
    print("  • Barra de estado con información en tiempo real")
    print()
    
    print("Para lanzar la GUI:")
    print("1. Instala las dependencias: ./setup.sh")
    print("2. Ejecuta con uv: uv run python main.py gui")
    print("   O activa el entorno: source .venv/bin/activate && python main.py gui")
    print()


def main():
    """Función principal del demo"""
    print("=" * 60)
    print("🎪 DEMO - Scripts CLI con Typer y tkinter")
    print("=" * 60)
    print()
    
    demo_cli()
    demo_gui_info()
    
    print("🛠️ Próximos pasos:")
    print("1. Ejecuta: ./setup.sh (para instalar dependencias)")
    print("2. Prueba la CLI: uv run python main.py --help")
    print("3. Lanza la GUI: uv run python main.py gui")
    print("4. O activa el entorno: source .venv/bin/activate")
    print()
    print("💡 Comandos útiles con uv:")
    print("• uv add [paquete]     - Añadir dependencia")
    print("• uv remove [paquete]  - Eliminar dependencia") 
    print("• uv run [comando]     - Ejecutar en el entorno")
    print("• uv sync              - Sincronizar dependencias")
    print()
    print("¡Disfruta desarrollando con Typer, tkinter y uv! 🚀")


if __name__ == "__main__":
    main()
