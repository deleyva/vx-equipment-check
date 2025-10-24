import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
from pathlib import Path


class ScriptsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Scripts CLI - Interfaz Gráfica")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Configurar el estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar el grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="🚀 Scripts CLI", 
            font=("Arial", 24, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Sección de saludo
        greeting_frame = ttk.LabelFrame(main_frame, text="Comando Hello", padding="10")
        greeting_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        greeting_frame.columnconfigure(1, weight=1)
        
        ttk.Label(greeting_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.name_entry = ttk.Entry(greeting_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Label(greeting_frame, text="Saludo:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.greeting_entry = ttk.Entry(greeting_frame, width=30)
        self.greeting_entry.insert(0, "Hola")
        self.greeting_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        
        hello_button = ttk.Button(
            greeting_frame, 
            text="Ejecutar Hello", 
            command=self.run_hello_command
        )
        hello_button.grid(row=0, column=2, rowspan=2, padx=(10, 0))
        
        # Sección de comandos rápidos
        commands_frame = ttk.LabelFrame(main_frame, text="Comandos Rápidos", padding="10")
        commands_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        info_button = ttk.Button(
            commands_frame, 
            text="📋 Mostrar Info", 
            command=self.run_info_command
        )
        info_button.grid(row=0, column=0, padx=(0, 10))
        
        help_button = ttk.Button(
            commands_frame, 
            text="❓ Ayuda", 
            command=self.show_help
        )
        help_button.grid(row=0, column=1, padx=(0, 10))
        
        clear_button = ttk.Button(
            commands_frame, 
            text="🗑️ Limpiar Output", 
            command=self.clear_output
        )
        clear_button.grid(row=0, column=2)
        
        # Área de salida
        output_frame = ttk.LabelFrame(main_frame, text="Salida de Comandos", padding="10")
        output_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame, 
            height=15, 
            wrap=tk.WORD,
            font=("Consolas", 10)
        )
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Barra de estado
        self.status_var = tk.StringVar()
        self.status_var.set("Listo")
        status_bar = ttk.Label(
            main_frame, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
    def run_hello_command(self):
        """Ejecuta el comando hello con los parámetros de la GUI"""
        name = self.name_entry.get().strip()
        greeting = self.greeting_entry.get().strip()
        
        if not name:
            messagebox.showwarning("Advertencia", "Por favor, introduce un nombre")
            return
            
        self.status_var.set("Ejecutando comando hello...")
        
        # Construir el comando
        cmd = ["python", "main.py", "hello", name]
        if greeting and greeting != "Hola":
            cmd.extend(["--greeting", greeting])
        
        self.run_command_async(cmd)
        
    def run_info_command(self):
        """Ejecuta el comando info"""
        self.status_var.set("Ejecutando comando info...")
        cmd = ["python", "main.py", "info"]
        self.run_command_async(cmd)
        
    def run_command_async(self, cmd):
        """Ejecuta un comando de forma asíncrona"""
        def run():
            try:
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    cwd=Path(__file__).parent
                )
                
                # Actualizar la GUI desde el hilo principal
                self.root.after(0, self.update_output, result)
                
            except Exception as e:
                error_msg = f"Error ejecutando comando: {str(e)}\n"
                self.root.after(0, self.update_output_error, error_msg)
        
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
        
    def update_output(self, result):
        """Actualiza el área de salida con el resultado del comando"""
        self.output_text.insert(tk.END, f"$ {' '.join(result.args)}\n")
        
        if result.stdout:
            self.output_text.insert(tk.END, result.stdout)
        
        if result.stderr:
            self.output_text.insert(tk.END, f"Error: {result.stderr}")
            
        if result.returncode != 0:
            self.output_text.insert(tk.END, f"Código de salida: {result.returncode}\n")
            
        self.output_text.insert(tk.END, "\n" + "="*50 + "\n\n")
        self.output_text.see(tk.END)
        self.status_var.set("Comando completado")
        
    def update_output_error(self, error_msg):
        """Actualiza el área de salida con un mensaje de error"""
        self.output_text.insert(tk.END, error_msg)
        self.output_text.see(tk.END)
        self.status_var.set("Error en comando")
        
    def clear_output(self):
        """Limpia el área de salida"""
        self.output_text.delete(1.0, tk.END)
        self.status_var.set("Output limpiado")
        
    def show_help(self):
        """Muestra la ayuda de la aplicación"""
        help_text = """
🚀 Scripts CLI - Ayuda

Esta interfaz gráfica te permite ejecutar comandos de la CLI de forma visual:

• Comando Hello: Saluda con un mensaje personalizado
• Mostrar Info: Muestra información sobre la aplicación
• Limpiar Output: Limpia el área de salida de comandos

También puedes usar la CLI directamente desde la terminal:
python main.py --help
        """
        messagebox.showinfo("Ayuda", help_text)


def launch_gui():
    """Función principal para lanzar la GUI"""
    root = tk.Tk()
    app = ScriptsGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.quit()


if __name__ == "__main__":
    launch_gui()
