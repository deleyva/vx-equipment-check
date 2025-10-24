#!/usr/bin/env python3
"""
Aplicación de verificación de equipos de escritorio
Permite al usuario reportar el estado de pantalla, teclado y ratón
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import ttkbootstrap as ttk_boot
from ttkbootstrap.constants import *
import json
from datetime import datetime
import os


class EquipmentCheckApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Verificación de Equipos - Control de Estado")
        self.root.geometry("600x700")
        
        # Variables para los checkboxes
        self.pantalla_estado = tk.StringVar(value="")
        self.teclado_estado = tk.StringVar(value="")
        self.raton_estado = tk.StringVar(value="")
        
        # Variables para las descripciones de problemas
        self.pantalla_problema = tk.StringVar()
        self.teclado_problema = tk.StringVar()
        self.raton_problema = tk.StringVar()
        
        # Referencias a los widgets de descripción
        self.pantalla_desc_frame = None
        self.teclado_desc_frame = None
        self.raton_desc_frame = None
        
        self.pantalla_desc_text = None
        self.teclado_desc_text = None
        self.raton_desc_text = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal con padding
        main_frame = ttk_boot.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Título
        title_label = ttk_boot.Label(
            main_frame,
            text="🖥️ Verificación de Estado de Equipos",
            font=("Arial", 18, "bold"),
            bootstyle=PRIMARY
        )
        title_label.pack(pady=(0, 20))
        
        # Subtítulo
        subtitle_label = ttk_boot.Label(
            main_frame,
            text="Por favor, indica el estado de cada componente del equipo:",
            font=("Arial", 11),
            bootstyle=SECONDARY
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Crear secciones para cada componente
        self.create_component_section(main_frame, "🖥️ Pantalla", self.pantalla_estado, "pantalla")
        self.create_component_section(main_frame, "⌨️ Teclado", self.teclado_estado, "teclado")
        self.create_component_section(main_frame, "🖱️ Ratón", self.raton_estado, "raton")
        
        # Botones de acción
        self.create_action_buttons(main_frame)
        
    def create_component_section(self, parent, title, estado_var, component_type):
        # Frame para cada componente
        component_frame = ttk_boot.LabelFrame(
            parent,
            text=title,
            padding=15,
            bootstyle=INFO
        )
        component_frame.pack(fill=X, pady=(0, 20))
        
        # Frame para los radiobuttons
        radio_frame = ttk_boot.Frame(component_frame)
        radio_frame.pack(fill=X, pady=(0, 10))
        
        # Radiobutton "Correcto"
        correcto_radio = ttk_boot.Radiobutton(
            radio_frame,
            text="✅ Correcto",
            variable=estado_var,
            value="correcto",
            bootstyle=SUCCESS,
            command=lambda: self.toggle_description(component_type, False)
        )
        correcto_radio.pack(side=LEFT, padx=(0, 20))
        
        # Radiobutton "Defectuoso"
        defectuoso_radio = ttk_boot.Radiobutton(
            radio_frame,
            text="❌ Defectuoso",
            variable=estado_var,
            value="defectuoso",
            bootstyle=DANGER,
            command=lambda: self.toggle_description(component_type, True)
        )
        defectuoso_radio.pack(side=LEFT)
        
        # Frame para la descripción del problema (inicialmente oculto)
        desc_frame = ttk_boot.Frame(component_frame)
        
        desc_label = ttk_boot.Label(
            desc_frame,
            text="Describe el problema:",
            font=("Arial", 10, "bold"),
            bootstyle=WARNING
        )
        desc_label.pack(anchor=W, pady=(10, 5))
        
        desc_text = tk.Text(
            desc_frame,
            height=3,
            width=50,
            wrap=tk.WORD,
            font=("Arial", 10),
            relief=tk.SOLID,
            borderwidth=1
        )
        desc_text.pack(fill=X, pady=(0, 5))
        
        # Guardar referencias
        if component_type == "pantalla":
            self.pantalla_desc_frame = desc_frame
            self.pantalla_desc_text = desc_text
        elif component_type == "teclado":
            self.teclado_desc_frame = desc_frame
            self.teclado_desc_text = desc_text
        elif component_type == "raton":
            self.raton_desc_frame = desc_frame
            self.raton_desc_text = desc_text
    
    def toggle_description(self, component_type, show):
        """Muestra u oculta el campo de descripción según el estado seleccionado"""
        desc_frame = None
        
        if component_type == "pantalla":
            desc_frame = self.pantalla_desc_frame
        elif component_type == "teclado":
            desc_frame = self.teclado_desc_frame
        elif component_type == "raton":
            desc_frame = self.raton_desc_frame
        
        if desc_frame:
            if show:
                desc_frame.pack(fill=X, pady=(10, 0))
            else:
                desc_frame.pack_forget()
                # Limpiar el texto cuando se oculta
                if component_type == "pantalla" and self.pantalla_desc_text:
                    self.pantalla_desc_text.delete(1.0, tk.END)
                elif component_type == "teclado" and self.teclado_desc_text:
                    self.teclado_desc_text.delete(1.0, tk.END)
                elif component_type == "raton" and self.raton_desc_text:
                    self.raton_desc_text.delete(1.0, tk.END)
    
    def create_action_buttons(self, parent):
        # Frame para botones
        button_frame = ttk_boot.Frame(parent)
        button_frame.pack(fill=X, pady=(20, 0))
        
        # Botón Limpiar
        clear_button = ttk_boot.Button(
            button_frame,
            text="🗑️ Limpiar Formulario",
            command=self.clear_form,
            bootstyle=SECONDARY,
            width=20
        )
        clear_button.pack(side=LEFT, padx=(0, 10))
        
        # Botón Enviar
        submit_button = ttk_boot.Button(
            button_frame,
            text="📤 Enviar Verificación",
            command=self.submit_form,
            bootstyle=SUCCESS,
            width=20
        )
        submit_button.pack(side=RIGHT)
    
    def clear_form(self):
        """Limpia todos los campos del formulario"""
        # Limpiar radiobuttons
        self.pantalla_estado.set("")
        self.teclado_estado.set("")
        self.raton_estado.set("")
        
        # Ocultar y limpiar campos de descripción
        self.toggle_description("pantalla", False)
        self.toggle_description("teclado", False)
        self.toggle_description("raton", False)
        
        messagebox.showinfo("✅ Formulario Limpiado", "Se han borrado todos los datos del formulario.")
    
    def validate_form(self):
        """Valida que todos los campos requeridos estén completos"""
        errors = []
        
        # Verificar que todos los componentes tengan estado seleccionado
        if not self.pantalla_estado.get():
            errors.append("• Selecciona el estado de la pantalla")
        
        if not self.teclado_estado.get():
            errors.append("• Selecciona el estado del teclado")
        
        if not self.raton_estado.get():
            errors.append("• Selecciona el estado del ratón")
        
        # Verificar que los componentes defectuosos tengan descripción
        if self.pantalla_estado.get() == "defectuoso":
            if not self.pantalla_desc_text.get(1.0, tk.END).strip():
                errors.append("• Describe el problema de la pantalla")
        
        if self.teclado_estado.get() == "defectuoso":
            if not self.teclado_desc_text.get(1.0, tk.END).strip():
                errors.append("• Describe el problema del teclado")
        
        if self.raton_estado.get() == "defectuoso":
            if not self.raton_desc_text.get(1.0, tk.END).strip():
                errors.append("• Describe el problema del ratón")
        
        return errors
    
    def generate_json_report(self):
        """Genera el reporte en formato JSON"""
        # Obtener descripciones de problemas
        pantalla_desc = self.pantalla_desc_text.get(1.0, tk.END).strip() if self.pantalla_estado.get() == "defectuoso" else ""
        teclado_desc = self.teclado_desc_text.get(1.0, tk.END).strip() if self.teclado_estado.get() == "defectuoso" else ""
        raton_desc = self.raton_desc_text.get(1.0, tk.END).strip() if self.raton_estado.get() == "defectuoso" else ""
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "verificacion_equipos": {
                "pantalla": {
                    "estado": self.pantalla_estado.get(),
                    "problema": pantalla_desc if pantalla_desc else None
                },
                "teclado": {
                    "estado": self.teclado_estado.get(),
                    "problema": teclado_desc if teclado_desc else None
                },
                "raton": {
                    "estado": self.raton_estado.get(),
                    "problema": raton_desc if raton_desc else None
                }
            },
            "resumen": {
                "total_componentes": 3,
                "componentes_correctos": sum(1 for estado in [self.pantalla_estado.get(), self.teclado_estado.get(), self.raton_estado.get()] if estado == "correcto"),
                "componentes_defectuosos": sum(1 for estado in [self.pantalla_estado.get(), self.teclado_estado.get(), self.raton_estado.get()] if estado == "defectuoso"),
                "equipo_operativo": all(estado == "correcto" for estado in [self.pantalla_estado.get(), self.teclado_estado.get(), self.raton_estado.get()])
            }
        }
        
        return report
    
    def submit_form(self):
        """Procesa el envío del formulario"""
        # Validar formulario
        errors = self.validate_form()
        
        if errors:
            error_message = "Por favor, completa los siguientes campos:\n\n" + "\n".join(errors)
            messagebox.showerror("❌ Formulario Incompleto", error_message)
            return
        
        # Generar reporte JSON
        report = self.generate_json_report()
        
        # Guardar en archivo
        filename = f"verificacion_equipos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            # Mostrar resultado
            self.show_result(report, filename)
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al guardar el archivo:\n{str(e)}")
    
    def show_result(self, report, filename):
        """Muestra el resultado en una ventana emergente"""
        # Crear ventana de resultado
        result_window = tk.Toplevel(self.root)
        result_window.title("✅ Verificación Completada")
        result_window.geometry("500x400")
        result_window.transient(self.root)
        result_window.grab_set()
        
        # Frame principal
        main_frame = ttk_boot.Frame(result_window, padding=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Título
        title_label = ttk_boot.Label(
            main_frame,
            text="✅ Verificación Enviada Correctamente",
            font=("Arial", 14, "bold"),
            bootstyle=SUCCESS
        )
        title_label.pack(pady=(0, 20))
        
        # Información del archivo
        file_label = ttk_boot.Label(
            main_frame,
            text=f"📁 Archivo guardado: {filename}",
            font=("Arial", 10),
            bootstyle=INFO
        )
        file_label.pack(pady=(0, 20))
        
        # Área de texto para mostrar el JSON
        json_text = scrolledtext.ScrolledText(
            main_frame,
            height=15,
            width=60,
            wrap=tk.WORD,
            font=("Consolas", 9)
        )
        json_text.pack(fill=BOTH, expand=True, pady=(0, 20))
        
        # Insertar JSON formateado
        json_formatted = json.dumps(report, indent=2, ensure_ascii=False)
        json_text.insert(1.0, json_formatted)
        json_text.config(state=tk.DISABLED)
        
        # Botón cerrar
        close_button = ttk_boot.Button(
            main_frame,
            text="🔙 Cerrar",
            command=result_window.destroy,
            bootstyle=PRIMARY
        )
        close_button.pack()


def main():
    """Función principal para lanzar la aplicación"""
    # Crear ventana principal con tema moderno
    root = ttk_boot.Window(themename="cosmo")  # Tema moderno y limpio
    
    # Configurar icono y propiedades de ventana
    root.resizable(True, True)
    root.minsize(600, 700)
    
    # Crear aplicación
    app = EquipmentCheckApp(root)
    
    # Centrar ventana en pantalla
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Iniciar aplicación
    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.quit()


if __name__ == "__main__":
    main()
