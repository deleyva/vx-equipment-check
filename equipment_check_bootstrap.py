#!/usr/bin/env python3
"""
Aplicación de verificación de equipos de escritorio - Versión ttkbootstrap simplificada
Paleta de colores VITALINUX: Naranja y Verde
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
from datetime import datetime


class VitalinuxEquipmentCheckApp:
    def __init__(self, root):
        self.root = root
        
        # Variables para los radiobuttons
        self.pantalla_estado = tk.StringVar(value="")
        self.teclado_estado = tk.StringVar(value="")
        self.raton_estado = tk.StringVar(value="")
        self.bateria_estado = tk.StringVar(value="")
        self.otros_estado = tk.StringVar(value="")
        
        # Referencias a los widgets de descripción
        self.pantalla_desc_text = None
        self.teclado_desc_text = None
        self.raton_desc_text = None
        self.bateria_desc_text = None
        self.otros_desc_text = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal con scroll usando ttkbootstrap
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Header
        self.create_header(main_frame)
        
        # Crear secciones para cada componente
        self.create_component_section(main_frame, "🖥️ Pantalla", self.pantalla_estado, "pantalla")
        self.create_component_section(main_frame, "⌨️ Teclado", self.teclado_estado, "teclado")
        self.create_component_section(main_frame, "🖱️ Ratón", self.raton_estado, "raton")
        self.create_component_section(main_frame, "🔋 Batería", self.bateria_estado, "bateria")
        self.create_component_section(main_frame, "⚙️ Otros", self.otros_estado, "otros")
        
        # Botones de acción
        self.create_action_buttons(main_frame)
        
    def create_header(self, parent):
        """Crea el header con estilo ttkbootstrap"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=X, pady=(0, 30))
        
        # Título principal
        title_label = ttk.Label(
            header_frame,
            text="🏢 VITALINUX",
            font=('Arial', 32, 'bold'),
            bootstyle="warning"  # Naranja
        )
        title_label.pack()
        
        # Subtítulo
        subtitle_label = ttk.Label(
            header_frame,
            text="Verificación de Estado de Equipos",
            font=('Arial', 24, 'bold'),
            bootstyle="success"  # Verde
        )
        subtitle_label.pack(pady=(10, 15))
        
        # Instrucciones
        instruction_label = ttk.Label(
            header_frame,
            text="Por favor, indica el estado de cada componente del equipo de trabajo:",
            font=('Arial', 16),
            bootstyle="secondary"
        )
        instruction_label.pack(pady=(15, 0))
        
    def create_component_section(self, parent, title, estado_var, component_type):
        # Frame para cada componente con estilo card
        component_frame = ttk.LabelFrame(
            parent,
            text=f"  {title}  ",
            padding=30,
            bootstyle="info"  # Estilo azul para las cards
        )
        component_frame.pack(fill=BOTH, expand=True, pady=(0, 25))
        
        # Frame para los radiobuttons
        radio_frame = ttk.Frame(component_frame)
        radio_frame.pack(fill=X, pady=(0, 15))
        
        # Radiobutton "Correcto" con estilo verde
        correcto_radio = ttk.Radiobutton(
            radio_frame,
            text="✅ Funcionamiento Correcto",
            variable=estado_var,
            value="correcto",
            bootstyle="success",
            command=lambda: self.toggle_description(component_type, False)
        )
        correcto_radio.pack(side=LEFT, padx=(0, 60))
        
        # Radiobutton "Defectuoso" con estilo rojo
        defectuoso_radio = ttk.Radiobutton(
            radio_frame,
            text="❌ Presenta Defectos",
            variable=estado_var,
            value="defectuoso",
            bootstyle="danger",
            command=lambda: self.toggle_description(component_type, True)
        )
        defectuoso_radio.pack(side=LEFT)
        
        # Frame para la descripción del problema (inicialmente oculto)
        desc_frame = ttk.Frame(component_frame)
        
        desc_label = ttk.Label(
            desc_frame,
            text="📝 Describe detalladamente el problema encontrado:",
            font=('Arial', 14, 'bold'),
            bootstyle="danger"
        )
        desc_label.pack(anchor=W, pady=(15, 8))
        
        # Campo de texto para descripción
        desc_text = tk.Text(
            desc_frame,
            height=5,
            wrap=tk.WORD,
            font=('Arial', 14),
            bg='#ffffff',
            fg='#495057',
            relief='solid',
            borderwidth=2
        )
        desc_text.pack(fill=BOTH, expand=True, pady=(0, 5))
        
        # Placeholder text
        placeholder = f"Ejemplo: {self.get_placeholder_text(component_type)}"
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
        elif component_type == "bateria":
            self.bateria_desc_frame = desc_frame
            self.bateria_desc_text = desc_text
        elif component_type == "otros":
            self.otros_desc_frame = desc_frame
            self.otros_desc_text = desc_text
    
    def get_placeholder_text(self, component_type):
        """Devuelve texto de placeholder específico para cada componente"""
        placeholders = {
            "pantalla": "La pantalla parpadea constantemente, hay líneas verticales en el lado derecho...",
            "teclado": "Algunas teclas no responden, la tecla espacio está atascada, falta la tecla Enter...",
            "raton": "El botón izquierdo no funciona bien, la rueda de scroll está bloqueada...",
            "bateria": "La batería se descarga muy rápido, no mantiene la carga, el indicador no funciona...",
            "otros": "Problemas con puertos USB, ventiladores hacen ruido, carcasa dañada, cables sueltos..."
        }
        return placeholders.get(component_type, "Describe el problema encontrado...")
    
    def clear_placeholder(self, text_widget, placeholder):
        """Limpia el placeholder cuando el usuario hace clic"""
        if text_widget.get(1.0, tk.END).strip() == placeholder:
            text_widget.delete(1.0, tk.END)
            text_widget.config(fg='#495057')
    
    def restore_placeholder(self, text_widget, placeholder):
        """Restaura el placeholder si el campo está vacío"""
        if not text_widget.get(1.0, tk.END).strip():
            text_widget.insert(1.0, placeholder)
            text_widget.config(fg='#6c757d')
    
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
        elif component_type == "bateria":
            desc_frame = self.bateria_desc_frame
            desc_text = self.bateria_desc_text
        elif component_type == "otros":
            desc_frame = self.otros_desc_frame
            desc_text = self.otros_desc_text
        
        if desc_frame:
            if show:
                desc_frame.pack(fill=X, pady=(10, 0))
            else:
                desc_frame.pack_forget()
                if desc_text:
                    desc_text.delete(1.0, tk.END)
                    placeholder = f"Ejemplo: {self.get_placeholder_text(component_type)}"
                    desc_text.insert(1.0, placeholder)
                    desc_text.config(fg='#6c757d')
    
    def create_action_buttons(self, parent):
        # Frame para botones
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=X, pady=(40, 0))
        
        # Container para botones
        button_container = ttk.Frame(button_frame)
        button_container.pack(fill=X, expand=True)
        
        # Botón Limpiar
        clear_button = ttk.Button(
            button_container,
            text="🗑️  Limpiar Formulario",
            command=self.clear_form,
            bootstyle="secondary-outline",
            width=25
        )
        clear_button.pack(side=LEFT, fill=X, expand=True, padx=(0, 15))
        
        # Botón Enviar
        submit_button = ttk.Button(
            button_container,
            text="📤  Enviar Verificación",
            command=self.submit_form,
            bootstyle="warning",  # Naranja sólido
            width=25
        )
        submit_button.pack(side=LEFT, fill=X, expand=True, padx=(15, 0))
    
    def clear_form(self):
        """Limpia todos los campos del formulario"""
        # Limpiar radiobuttons
        self.pantalla_estado.set("")
        self.teclado_estado.set("")
        self.raton_estado.set("")
        self.bateria_estado.set("")
        self.otros_estado.set("")
        
        # Ocultar campos de descripción
        self.toggle_description("pantalla", False)
        self.toggle_description("teclado", False)
        self.toggle_description("raton", False)
        self.toggle_description("bateria", False)
        self.toggle_description("otros", False)
        
        messagebox.showinfo("✅ Formulario Limpiado", 
                          "Se han borrado todos los datos del formulario.")
    
    def get_description_text(self, text_widget):
        """Obtiene el texto real del widget, excluyendo placeholders"""
        content = text_widget.get(1.0, tk.END).strip()
        
        placeholders = [
            f"Ejemplo: {self.get_placeholder_text('pantalla')}",
            f"Ejemplo: {self.get_placeholder_text('teclado')}",
            f"Ejemplo: {self.get_placeholder_text('raton')}",
            f"Ejemplo: {self.get_placeholder_text('bateria')}",
            f"Ejemplo: {self.get_placeholder_text('otros')}"
        ]
        
        if content in placeholders or not content:
            return ""
        return content
    
    def validate_form(self):
        """Valida que todos los campos requeridos estén completos"""
        errors = []
        
        # Verificar que los componentes OBLIGATORIOS tengan estado seleccionado
        if not self.pantalla_estado.get():
            errors.append("• Selecciona el estado de la pantalla (obligatorio)")
        
        if not self.teclado_estado.get():
            errors.append("• Selecciona el estado del teclado (obligatorio)")
        
        # Verificar que los componentes defectuosos tengan descripción
        if self.pantalla_estado.get() == "defectuoso":
            if not self.get_description_text(self.pantalla_desc_text):
                errors.append("• Describe el problema de la pantalla")
        
        if self.teclado_estado.get() == "defectuoso":
            if not self.get_description_text(self.teclado_desc_text):
                errors.append("• Describe el problema del teclado")
        
        # Verificar componentes OPCIONALES solo si están seleccionados como defectuosos
        if self.raton_estado.get() == "defectuoso":
            if not self.get_description_text(self.raton_desc_text):
                errors.append("• Describe el problema del ratón")
        
        if self.bateria_estado.get() == "defectuoso":
            if not self.get_description_text(self.bateria_desc_text):
                errors.append("• Describe el problema de la batería")
        
        if self.otros_estado.get() == "defectuoso":
            if not self.get_description_text(self.otros_desc_text):
                errors.append("• Describe el problema en la sección 'Otros'")
        
        return errors
    
    def generate_json_report(self):
        """Genera el reporte en formato JSON"""
        # Obtener descripciones de problemas
        pantalla_desc = self.get_description_text(self.pantalla_desc_text) if self.pantalla_estado.get() == "defectuoso" else ""
        teclado_desc = self.get_description_text(self.teclado_desc_text) if self.teclado_estado.get() == "defectuoso" else ""
        raton_desc = self.get_description_text(self.raton_desc_text) if self.raton_estado.get() == "defectuoso" else ""
        bateria_desc = self.get_description_text(self.bateria_desc_text) if self.bateria_estado.get() == "defectuoso" else ""
        otros_desc = self.get_description_text(self.otros_desc_text) if self.otros_estado.get() == "defectuoso" else ""
        
        # Obtener todos los estados
        estados = [
            self.pantalla_estado.get(),
            self.teclado_estado.get(),
            self.raton_estado.get() if self.raton_estado.get() else None,
            self.bateria_estado.get() if self.bateria_estado.get() else None,
            self.otros_estado.get() if self.otros_estado.get() else None
        ]
        
        estados_validos = [estado for estado in estados if estado]
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "empresa": "VITALINUX",
            "tipo_verificacion": "equipos_escritorio",
            "usuario": "usuario_actual",
            "verificacion_equipos": {
                "pantalla": {
                    "estado": self.pantalla_estado.get(),
                    "problema": pantalla_desc if pantalla_desc else None,
                    "obligatorio": True
                },
                "teclado": {
                    "estado": self.teclado_estado.get(),
                    "problema": teclado_desc if teclado_desc else None,
                    "obligatorio": True
                },
                "raton": {
                    "estado": self.raton_estado.get() if self.raton_estado.get() else "no_verificado",
                    "problema": raton_desc if raton_desc else None,
                    "obligatorio": False
                },
                "bateria": {
                    "estado": self.bateria_estado.get() if self.bateria_estado.get() else "no_verificado",
                    "problema": bateria_desc if bateria_desc else None,
                    "obligatorio": False
                },
                "otros": {
                    "estado": self.otros_estado.get() if self.otros_estado.get() else "no_verificado",
                    "problema": otros_desc if otros_desc else None,
                    "obligatorio": False
                }
            },
            "resumen": {
                "total_componentes": 5,
                "componentes_obligatorios": 2,
                "componentes_opcionales": 3,
                "componentes_verificados": len(estados_validos),
                "componentes_correctos": sum(1 for estado in estados_validos if estado == "correcto"),
                "componentes_defectuosos": sum(1 for estado in estados_validos if estado == "defectuoso"),
                "equipo_operativo": all(estado in ["correcto", "no_verificado", None] for estado in estados),
                "requiere_atencion": any(estado == "defectuoso" for estado in estados_validos)
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
        filename = f"vitalinux_verificacion_equipos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
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
        result_window.title("✅ VITALINUX - Verificación Completada")
        result_window.geometry("650x600")
        result_window.transient(self.root)
        result_window.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(result_window, padding=25)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame,
            text="✅ VERIFICACIÓN COMPLETADA",
            font=('Arial', 18, 'bold'),
            bootstyle="success"
        )
        title_label.pack(pady=(0, 15))
        
        # Información del archivo
        file_label = ttk.Label(
            main_frame,
            text=f"📁 Archivo guardado: {filename}",
            font=('Arial', 12),
            bootstyle="info"
        )
        file_label.pack(pady=(0, 20))
        
        # Resumen del estado
        resumen = report["resumen"]
        if resumen["equipo_operativo"]:
            status_text = "🟢 EQUIPO OPERATIVO"
            status_style = "success"
        else:
            status_text = "🟠 REQUIERE ATENCIÓN"
            status_style = "warning"
        
        status_label = ttk.Label(
            main_frame,
            text=status_text,
            font=('Arial', 14, 'bold'),
            bootstyle=status_style
        )
        status_label.pack(pady=(0, 10))
        
        summary_label = ttk.Label(
            main_frame,
            text=f"Componentes correctos: {resumen['componentes_correctos']}/{resumen['componentes_verificados']} | Defectuosos: {resumen['componentes_defectuosos']}/{resumen['componentes_verificados']}",
            font=('Arial', 11),
            bootstyle="secondary"
        )
        summary_label.pack(pady=(0, 20))
        
        # Área de texto para mostrar el JSON
        json_label = ttk.Label(
            main_frame,
            text="📄 Datos del reporte (JSON):",
            font=('Arial', 12, 'bold')
        )
        json_label.pack(anchor=W, pady=(0, 8))
        
        json_text = scrolledtext.ScrolledText(
            main_frame,
            height=15,
            width=70,
            wrap=tk.WORD,
            font=('Consolas', 10)
        )
        json_text.pack(fill=BOTH, expand=True, pady=(0, 20))
        
        # Insertar JSON formateado
        json_formatted = json.dumps(report, indent=2, ensure_ascii=False)
        json_text.insert(1.0, json_formatted)
        json_text.config(state=tk.DISABLED)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X)
        
        # Botón nueva verificación
        new_button = ttk.Button(
            button_frame,
            text="🔄 Nueva Verificación",
            command=lambda: [result_window.destroy(), self.clear_form()],
            bootstyle="primary",
            width=20
        )
        new_button.pack(side=LEFT)
        
        # Botón cerrar
        close_button = ttk.Button(
            button_frame,
            text="🔙 Cerrar",
            command=result_window.destroy,
            bootstyle="secondary",
            width=20
        )
        close_button.pack(side=RIGHT)


def main():
    """Función principal para lanzar la aplicación"""
    # Crear ventana principal con ttkbootstrap
    root = ttk.Window(
        title="VITALINUX - Verificación de Equipos",
        themename="cosmo",  # Tema moderno y limpio
        size=(1200, 900),
        resizable=(True, True)
    )
    
    # Configurar propiedades de ventana
    root.minsize(800, 600)
    
    # Crear aplicación
    app = VitalinuxEquipmentCheckApp(root)
    
    # Centrar ventana en pantalla
    root.place_window_center()
    
    # Iniciar aplicación
    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.quit()


if __name__ == "__main__":
    main()
