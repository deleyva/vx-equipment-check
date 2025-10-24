#!/usr/bin/env python3
"""
Aplicación de verificación de equipos de escritorio - Versión Estilizada
Paleta de colores VITALINUX: Naranja (#FF6B35, #FF8C42) y Verde (#4CAF50, #2E7D32)
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from datetime import datetime


class MigasEquipmentCheckApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VITALINUX - Verificación de Equipos")
        
        # Configurar para pantalla completa
        self.root.state('zoomed')  # Windows
        try:
            self.root.attributes('-zoomed', True)  # Linux
        except:
            pass
        try:
            self.root.attributes('-fullscreen', False)  # Mantener barra de título
        except:
            pass
        
        self.root.configure(bg='#f8f9fa')
        
        # Paleta de colores Migas
        self.colors = {
            'primary_orange': '#FF6B35',
            'secondary_orange': '#FF8C42', 
            'primary_green': '#4CAF50',
            'secondary_green': '#2E7D32',
            'light_gray': '#f8f9fa',
            'medium_gray': '#e9ecef',
            'dark_gray': '#495057',
            'white': '#ffffff',
            'danger': '#dc3545',
            'warning': '#ffc107',
            'success': '#28a745'
        }
        
        # Variables para los radiobuttons
        self.pantalla_estado = tk.StringVar(value="")
        self.teclado_estado = tk.StringVar(value="")
        self.raton_estado = tk.StringVar(value="")
        self.bateria_estado = tk.StringVar(value="")
        self.otros_estado = tk.StringVar(value="")
        
        # Referencias a los widgets de descripción
        self.pantalla_desc_frame = None
        self.teclado_desc_frame = None
        self.raton_desc_frame = None
        self.bateria_desc_frame = None
        self.otros_desc_frame = None
        
        self.pantalla_desc_text = None
        self.teclado_desc_text = None
        self.raton_desc_text = None
        self.bateria_desc_text = None
        self.otros_desc_text = None
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        """Configura los estilos personalizados con la paleta VITALINUX"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Los estilos se aplican directamente en los widgets
        # usando parámetros como font y foreground
        
    def create_widgets(self):
        # Crear canvas y scrollbar para scroll vertical
        canvas = tk.Canvas(self.root, bg='#f8f9fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Configurar el scroll
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configurar el canvas para que el frame use todo el ancho
        def configure_canvas_width(event):
            canvas.itemconfig(canvas.find_all()[0], width=event.width)
        
        canvas.bind('<Configure>', configure_canvas_width)
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame principal con padding mínimo para maximizar ancho
        main_frame = ttk.Frame(scrollable_frame, padding=(10, 30, 10, 30))
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header con logo/título
        self.create_header(main_frame)
        
        # Crear secciones para cada componente
        self.create_component_section(main_frame, "🖥️ Pantalla", self.pantalla_estado, "pantalla")
        self.create_component_section(main_frame, "⌨️ Teclado", self.teclado_estado, "teclado")
        self.create_component_section(main_frame, "🖱️ Ratón", self.raton_estado, "raton")
        self.create_component_section(main_frame, "🔋 Batería", self.bateria_estado, "bateria")
        self.create_component_section(main_frame, "⚙️ Otros", self.otros_estado, "otros")
        
        # Botones de acción
        self.create_action_buttons(main_frame)
        
        # Configurar scroll con rueda del ratón
        self.bind_mousewheel(canvas)
    
    def bind_mousewheel(self, canvas):
        """Scroll simple: arriba va al principio, abajo va al final"""
        def _on_mousewheel(event):
            # Scroll simple: arriba = principio, abajo = final
            if event.delta > 0 or (hasattr(event, 'num') and event.num == 4):
                # Scroll hacia arriba = ir al principio
                canvas.yview_moveto(0)
            elif event.delta < 0 or (hasattr(event, 'num') and event.num == 5):
                # Scroll hacia abajo = ir al final
                canvas.yview_moveto(1)
        
        # Bind simple a todos los eventos de scroll
        canvas.bind("<MouseWheel>", _on_mousewheel)
        canvas.bind("<Button-4>", _on_mousewheel)
        canvas.bind("<Button-5>", _on_mousewheel)
        self.root.bind("<MouseWheel>", _on_mousewheel)
        self.root.bind("<Button-4>", _on_mousewheel)
        self.root.bind("<Button-5>", _on_mousewheel)
        
    def create_header(self, parent):
        """Crea el header con estilo estándar"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Título principal
        title_label = ttk.Label(
            header_frame,
            text="🏢 VITALINUX",
            font=('Arial', 32, 'bold'),
            foreground="#FF6B35"  # Naranja
        )
        title_label.pack()
        
        # Subtítulo
        subtitle_label = ttk.Label(
            header_frame,
            text="Verificación de Estado de Equipos",
            font=('Arial', 24, 'bold'),
            foreground="#2E7D32"  # Verde
        )
        subtitle_label.pack(pady=(10, 15))
        
        # Línea separadora
        separator = ttk.Separator(header_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=(10, 0))
        
        # Instrucciones
        instruction_label = ttk.Label(
            header_frame,
            text="Por favor, indica el estado de cada componente del equipo de trabajo:",
            font=('Arial', 16),
            foreground="#495057"
        )
        instruction_label.pack(pady=(15, 0))
        
    def create_component_section(self, parent, title, estado_var, component_type):
        # Frame para cada componente con estilo card
        component_frame = ttk.LabelFrame(
            parent,
            text=f"  {title}  ",
            padding=30
        )
        component_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 25), padx=0)
        
        # Frame para los radiobuttons
        radio_frame = ttk.Frame(component_frame)
        radio_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Radiobutton "Correcto" con estilo verde
        correcto_radio = ttk.Radiobutton(
            radio_frame,
            text="✅ Funcionamiento Correcto",
            variable=estado_var,
            value="correcto",
            command=lambda: self.toggle_description(component_type, False)
        )
        correcto_radio.pack(side=tk.LEFT, padx=(0, 60))
        
        # Radiobutton "Defectuoso" con estilo rojo
        defectuoso_radio = ttk.Radiobutton(
            radio_frame,
            text="❌ Presenta Defectos",
            variable=estado_var,
            value="defectuoso",
            command=lambda: self.toggle_description(component_type, True)
        )
        defectuoso_radio.pack(side=tk.LEFT)
        
        # Frame para la descripción del problema (inicialmente oculto)
        desc_frame = ttk.Frame(component_frame)
        
        # Línea separadora
        separator = ttk.Separator(desc_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=(10, 15))
        
        desc_label = ttk.Label(
            desc_frame,
            text="📝 Describe detalladamente el problema encontrado:",
            font=('Arial', 14, 'bold'),
            foreground="#dc3545"
        )
        desc_label.pack(anchor=tk.W, pady=(0, 8))
        
        # Frame para el textarea con borde personalizado
        text_container = tk.Frame(desc_frame, 
                                 bg=self.colors['white'], 
                                 relief='solid', 
                                 borderwidth=2,
                                 highlightbackground=self.colors['primary_orange'],
                                 highlightthickness=1)
        text_container.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        desc_text = tk.Text(
            text_container,
            height=5,
            wrap=tk.WORD,
            font=('Arial', 14),
            bg=self.colors['white'],
            fg=self.colors['dark_gray'],
            relief='flat',
            borderwidth=8,
            selectbackground=self.colors['secondary_orange'],
            selectforeground=self.colors['white']
        )
        desc_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
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
            "pantalla": "La pantalla parpadea constantemente, hay líneas verticales en el lado derecho, el brillo no se ajusta...",
            "teclado": "Algunas teclas no responden, la tecla espacio está atascada, falta la tecla Enter...",
            "raton": "El botón izquierdo no funciona bien, la rueda de scroll está bloqueada, el cursor se mueve lentamente...",
            "bateria": "La batería se descarga muy rápido, no mantiene la carga, el indicador no funciona correctamente...",
            "otros": "Problemas con puertos USB, ventiladores hacen ruido, carcasa dañada, cables sueltos..."
        }
        return placeholders.get(component_type, "Describe el problema encontrado...")
    
    def clear_placeholder(self, text_widget, placeholder):
        """Limpia el placeholder cuando el usuario hace clic"""
        if text_widget.get(1.0, tk.END).strip() == placeholder:
            text_widget.delete(1.0, tk.END)
            text_widget.config(fg=self.colors['dark_gray'])
    
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
                desc_frame.pack(fill=tk.X, pady=(10, 0))
            else:
                desc_frame.pack_forget()
                # Restaurar placeholder cuando se oculta
                if desc_text:
                    desc_text.delete(1.0, tk.END)
                    placeholder = f"Ejemplo: {self.get_placeholder_text(component_type)}"
                    desc_text.insert(1.0, placeholder)
                    desc_text.config(fg='#6c757d')
    
    def create_action_buttons(self, parent):
        # Frame para botones con estilo
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(40, 0))
        
        # Línea separadora superior
        separator = ttk.Separator(button_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=(0, 20))
        
        # Container para botones que ocupe todo el ancho
        button_container = ttk.Frame(button_frame)
        button_container.pack(fill=tk.X, expand=True)
        
        # Botón Limpiar
        clear_button = ttk.Button(
            button_container,
            text="🗑️  Limpiar Formulario",
            command=self.clear_form,
            width=25
        )
        clear_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        
        # Botón Enviar
        submit_button = ttk.Button(
            button_container,
            text="📤  Enviar Verificación",
            command=self.submit_form,
            width=25
        )
        submit_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(15, 0))
    
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
                          "Se han borrado todos los datos del formulario.",
                          icon='info')
    
    def get_description_text(self, text_widget):
        """Obtiene el texto real del widget, excluyendo placeholders"""
        content = text_widget.get(1.0, tk.END).strip()
        
        # Lista de placeholders
        placeholders = [
            f"Ejemplo: {self.get_placeholder_text('pantalla')}",
            f"Ejemplo: {self.get_placeholder_text('teclado')}",
            f"Ejemplo: {self.get_placeholder_text('raton')}"
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
        
        # Obtener todos los estados (incluyendo vacíos para opcionales)
        estados = [
            self.pantalla_estado.get(),
            self.teclado_estado.get(),
            self.raton_estado.get() if self.raton_estado.get() else None,
            self.bateria_estado.get() if self.bateria_estado.get() else None,
            self.otros_estado.get() if self.otros_estado.get() else None
        ]
        
        # Filtrar estados válidos para el conteo
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
        filename = f"migas_verificacion_equipos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            # Mostrar resultado
            self.show_result(report, filename)
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al guardar el archivo:\n{str(e)}")
    
    def show_result(self, report, filename):
        """Muestra el resultado en una ventana emergente con estilo Migas"""
        # Crear ventana de resultado
        result_window = tk.Toplevel(self.root)
        result_window.title("✅ Migas - Verificación Completada")
        result_window.geometry("650x600")
        result_window.transient(self.root)
        result_window.grab_set()
        result_window.configure(bg=self.colors['light_gray'])
        
        # Frame principal
        main_frame = ttk.Frame(result_window, style='Main.TFrame', padding=25)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header de resultado
        header_frame = ttk.Frame(main_frame, style='Main.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Título
        title_label = ttk.Label(
            header_frame,
            text="✅ VERIFICACIÓN COMPLETADA",
            font=('Arial', 18, 'bold'),
            background=self.colors['light_gray'],
            foreground=self.colors['primary_green']
        )
        title_label.pack()
        
        # Subtítulo con empresa
        company_label = ttk.Label(
            header_frame,
            text="🏢 VITALINUX - Sistema de Verificación de Equipos",
            font=('Arial', 12),
            background=self.colors['light_gray'],
            foreground=self.colors['secondary_green']
        )
        company_label.pack(pady=(5, 15))
        
        # Información del archivo
        file_frame = tk.Frame(main_frame, bg=self.colors['white'], relief='solid', borderwidth=1)
        file_frame.pack(fill=tk.X, pady=(0, 20))
        
        file_label = ttk.Label(
            file_frame,
            text=f"📁 Archivo guardado: {filename}",
            font=('Arial', 11, 'bold'),
            background=self.colors['white'],
            foreground=self.colors['dark_gray']
        )
        file_label.pack(pady=10)
        
        # Resumen del estado con colores
        resumen = report["resumen"]
        status_frame = tk.Frame(main_frame, bg=self.colors['white'], relief='solid', borderwidth=2)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        if resumen["equipo_operativo"]:
            status_color = self.colors['primary_green']
            status_text = "🟢 EQUIPO OPERATIVO"
            status_bg = '#d4edda'
        else:
            status_color = self.colors['primary_orange']
            status_text = "🟠 REQUIERE ATENCIÓN"
            status_bg = '#fff3cd'
        
        status_frame.configure(bg=status_bg)
        
        status_label = ttk.Label(
            status_frame,
            text=status_text,
            font=('Arial', 14, 'bold'),
            background=status_bg,
            foreground=status_color
        )
        status_label.pack(pady=15)
        
        summary_label = ttk.Label(
            status_frame,
            text=f"Componentes correctos: {resumen['componentes_correctos']}/3 | Defectuosos: {resumen['componentes_defectuosos']}/3",
            font=('Arial', 11),
            background=status_bg,
            foreground=self.colors['dark_gray']
        )
        summary_label.pack(pady=(0, 15))
        
        # Área de texto para mostrar el JSON
        json_label = ttk.Label(
            main_frame,
            text="📄 Datos del reporte (JSON):",
            font=('Arial', 12, 'bold'),
            background=self.colors['light_gray'],
            foreground=self.colors['secondary_green']
        )
        json_label.pack(anchor=tk.W, pady=(0, 8))
        
        # Container para el JSON con borde
        json_container = tk.Frame(main_frame, bg=self.colors['white'], relief='solid', borderwidth=2)
        json_container.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        json_text = scrolledtext.ScrolledText(
            json_container,
            height=12,
            width=75,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg=self.colors['white'],
            fg=self.colors['dark_gray'],
            relief='flat',
            borderwidth=5,
            selectbackground=self.colors['secondary_orange']
        )
        json_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Insertar JSON formateado
        json_formatted = json.dumps(report, indent=2, ensure_ascii=False)
        json_text.insert(1.0, json_formatted)
        json_text.config(state=tk.DISABLED)
        
        # Botones con estilo
        button_frame = ttk.Frame(main_frame, style='Main.TFrame')
        button_frame.pack(fill=tk.X)
        
        # Botón nueva verificación
        new_button = ttk.Button(
            button_frame,
            text="🔄  Nueva Verificación",
            command=lambda: [result_window.destroy(), self.clear_form()],
            style='Primary.TButton',
            width=22
        )
        new_button.pack(side=tk.LEFT)
        
        # Botón cerrar
        close_button = ttk.Button(
            button_frame,
            text="🔙  Cerrar",
            command=result_window.destroy,
            style='Secondary.TButton',
            width=22
        )
        close_button.pack(side=tk.RIGHT)


def main():
    """Función principal para lanzar la aplicación"""
    # Crear ventana principal
    root = tk.Tk()
    
    # Configurar propiedades de ventana
    root.resizable(True, True)
    root.minsize(650, 750)
    
    # Crear aplicación
    app = MigasEquipmentCheckApp(root)
    
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
