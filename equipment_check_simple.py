#!/usr/bin/env python3
"""
Aplicación de verificación de equipos de escritorio
Permite al usuario reportar el estado de pantalla, teclado y ratón
Versión simple con tkinter estándar
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from datetime import datetime


class EquipmentCheckApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Verificación de Equipos - Control de Estado")
        self.root.geometry("650x750")
        self.root.configure(bg='#f0f0f0')
        
        # Variables para los radiobuttons
        self.pantalla_estado = tk.StringVar(value="")
        self.teclado_estado = tk.StringVar(value="")
        self.raton_estado = tk.StringVar(value="")
        
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
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame,
            text="🖥️ Verificación de Estado de Equipos",
            font=("Arial", 18, "bold"),
            foreground="#2c3e50"
        )
        title_label.pack(pady=(0, 10))
        
        # Subtítulo
        subtitle_label = ttk.Label(
            main_frame,
            text="Por favor, indica el estado de cada componente del equipo:",
            font=("Arial", 11),
            foreground="#7f8c8d"
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
        component_frame = ttk.LabelFrame(
            parent,
            text=title,
            padding=15
        )
        component_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Frame para los radiobuttons
        radio_frame = ttk.Frame(component_frame)
        radio_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Radiobutton "Correcto"
        correcto_radio = ttk.Radiobutton(
            radio_frame,
            text="✅ Correcto",
            variable=estado_var,
            value="correcto",
            command=lambda: self.toggle_description(component_type, False)
        )
        correcto_radio.pack(side=tk.LEFT, padx=(0, 30))
        
        # Radiobutton "Defectuoso"
        defectuoso_radio = ttk.Radiobutton(
            radio_frame,
            text="❌ Defectuoso",
            variable=estado_var,
            value="defectuoso",
            command=lambda: self.toggle_description(component_type, True)
        )
        defectuoso_radio.pack(side=tk.LEFT)
        
        # Frame para la descripción del problema (inicialmente oculto)
        desc_frame = ttk.Frame(component_frame)
        
        desc_label = ttk.Label(
            desc_frame,
            text="Describe el problema encontrado:",
            font=("Arial", 10, "bold"),
            foreground="#e74c3c"
        )
        desc_label.pack(anchor=tk.W, pady=(10, 5))
        
        desc_text = tk.Text(
            desc_frame,
            height=4,
            width=60,
            wrap=tk.WORD,
            font=("Arial", 10),
            relief=tk.SOLID,
            borderwidth=1,
            bg="#fff3cd",
            fg="#856404"
        )
        desc_text.pack(fill=tk.X, pady=(0, 5))
        
        # Placeholder text
        placeholder = "Ejemplo: La pantalla parpadea constantemente, hay líneas verticales en el lado derecho..."
        desc_text.insert(1.0, placeholder)
        desc_text.bind("<FocusIn>", lambda e: self.clear_placeholder(desc_text, placeholder))
        desc_text.bind("<FocusOut>", lambda e: self.restore_placeholder(desc_text, placeholder))
        
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
    
    def clear_placeholder(self, text_widget, placeholder):
        """Limpia el placeholder cuando el usuario hace clic"""
        if text_widget.get(1.0, tk.END).strip() == placeholder:
            text_widget.delete(1.0, tk.END)
            text_widget.config(fg="#000000")
    
    def restore_placeholder(self, text_widget, placeholder):
        """Restaura el placeholder si el campo está vacío"""
        if not text_widget.get(1.0, tk.END).strip():
            text_widget.insert(1.0, placeholder)
            text_widget.config(fg="#856404")
    
    def toggle_description(self, component_type, show):
        """Muestra u oculta el campo de descripción según el estado seleccionado"""
        desc_frame = None
        desc_text = None
        
        if component_type == "pantalla":
            desc_frame = self.pantalla_desc_frame
            desc_text = self.pantalla_desc_text
        elif component_type == "teclado":
            desc_frame = self.teclado_desc_frame
            desc_text = self.teclado_desc_text
        elif component_type == "raton":
            desc_frame = self.raton_desc_frame
            desc_text = self.raton_desc_text
        
        if desc_frame:
            if show:
                desc_frame.pack(fill=tk.X, pady=(10, 0))
            else:
                desc_frame.pack_forget()
                # Restaurar placeholder cuando se oculta
                if desc_text:
                    desc_text.delete(1.0, tk.END)
                    placeholder = "Ejemplo: La pantalla parpadea constantemente, hay líneas verticales en el lado derecho..."
                    desc_text.insert(1.0, placeholder)
                    desc_text.config(fg="#856404")
    
    def create_action_buttons(self, parent):
        # Frame para botones
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(30, 0))
        
        # Botón Limpiar
        clear_button = ttk.Button(
            button_frame,
            text="🗑️ Limpiar Formulario",
            command=self.clear_form,
            width=25
        )
        clear_button.pack(side=tk.LEFT, padx=(0, 20))
        
        # Botón Enviar
        submit_button = ttk.Button(
            button_frame,
            text="📤 Enviar Verificación",
            command=self.submit_form,
            width=25
        )
        submit_button.pack(side=tk.RIGHT)
        
        # Configurar estilo de botón enviar
        submit_button.configure(style="Accent.TButton")
    
    def clear_form(self):
        """Limpia todos los campos del formulario"""
        # Limpiar radiobuttons
        self.pantalla_estado.set("")
        self.teclado_estado.set("")
        self.raton_estado.set("")
        
        # Ocultar campos de descripción
        self.toggle_description("pantalla", False)
        self.toggle_description("teclado", False)
        self.toggle_description("raton", False)
        
        messagebox.showinfo("✅ Formulario Limpiado", "Se han borrado todos los datos del formulario.")
    
    def get_description_text(self, text_widget):
        """Obtiene el texto real del widget, excluyendo placeholders"""
        content = text_widget.get(1.0, tk.END).strip()
        placeholders = [
            "Ejemplo: La pantalla parpadea constantemente, hay líneas verticales en el lado derecho..."
        ]
        
        if content in placeholders or not content:
            return ""
        return content
    
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
            if not self.get_description_text(self.pantalla_desc_text):
                errors.append("• Describe el problema de la pantalla")
        
        if self.teclado_estado.get() == "defectuoso":
            if not self.get_description_text(self.teclado_desc_text):
                errors.append("• Describe el problema del teclado")
        
        if self.raton_estado.get() == "defectuoso":
            if not self.get_description_text(self.raton_desc_text):
                errors.append("• Describe el problema del ratón")
        
        return errors
    
    def generate_json_report(self):
        """Genera el reporte en formato JSON"""
        # Obtener descripciones de problemas
        pantalla_desc = self.get_description_text(self.pantalla_desc_text) if self.pantalla_estado.get() == "defectuoso" else ""
        teclado_desc = self.get_description_text(self.teclado_desc_text) if self.teclado_estado.get() == "defectuoso" else ""
        raton_desc = self.get_description_text(self.raton_desc_text) if self.raton_estado.get() == "defectuoso" else ""
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "usuario": "usuario_actual",  # Puedes modificar esto para obtener el usuario real
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
        result_window.geometry("600x500")
        result_window.transient(self.root)
        result_window.grab_set()
        result_window.configure(bg='#f8f9fa')
        
        # Frame principal
        main_frame = ttk.Frame(result_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame,
            text="✅ Verificación Enviada Correctamente",
            font=("Arial", 16, "bold"),
            foreground="#28a745"
        )
        title_label.pack(pady=(0, 15))
        
        # Información del archivo
        file_label = ttk.Label(
            main_frame,
            text=f"📁 Archivo guardado: {filename}",
            font=("Arial", 11),
            foreground="#6c757d"
        )
        file_label.pack(pady=(0, 20))
        
        # Resumen del estado
        resumen = report["resumen"]
        status_color = "#28a745" if resumen["equipo_operativo"] else "#dc3545"
        status_text = "OPERATIVO" if resumen["equipo_operativo"] else "REQUIERE ATENCIÓN"
        
        status_label = ttk.Label(
            main_frame,
            text=f"Estado del equipo: {status_text}",
            font=("Arial", 12, "bold"),
            foreground=status_color
        )
        status_label.pack(pady=(0, 10))
        
        summary_label = ttk.Label(
            main_frame,
            text=f"Componentes correctos: {resumen['componentes_correctos']}/3 | Defectuosos: {resumen['componentes_defectuosos']}/3",
            font=("Arial", 10),
            foreground="#6c757d"
        )
        summary_label.pack(pady=(0, 20))
        
        # Área de texto para mostrar el JSON
        json_label = ttk.Label(
            main_frame,
            text="📄 Datos del reporte (JSON):",
            font=("Arial", 11, "bold")
        )
        json_label.pack(anchor=tk.W, pady=(0, 5))
        
        json_text = scrolledtext.ScrolledText(
            main_frame,
            height=15,
            width=70,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#f8f9fa",
            fg="#495057"
        )
        json_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Insertar JSON formateado
        json_formatted = json.dumps(report, indent=2, ensure_ascii=False)
        json_text.insert(1.0, json_formatted)
        json_text.config(state=tk.DISABLED)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # Botón nueva verificación
        new_button = ttk.Button(
            button_frame,
            text="🔄 Nueva Verificación",
            command=lambda: [result_window.destroy(), self.clear_form()],
            width=20
        )
        new_button.pack(side=tk.LEFT)
        
        # Botón cerrar
        close_button = ttk.Button(
            button_frame,
            text="🔙 Cerrar",
            command=result_window.destroy,
            width=20
        )
        close_button.pack(side=tk.RIGHT)


def main():
    """Función principal para lanzar la aplicación"""
    # Crear ventana principal
    root = tk.Tk()
    
    # Configurar propiedades de ventana
    root.resizable(True, True)
    root.minsize(650, 750)
    
    # Configurar estilo ttk
    style = ttk.Style()
    style.theme_use('clam')
    
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
