# 🖥️ Aplicación de Verificación de Equipos

Una aplicación de escritorio con GUI para verificar el estado de los equipos de trabajo (pantalla, teclado y ratón).

## 📋 Características

- ✅ **Interfaz gráfica moderna** con tkinter
- 🔘 **Checkboxes intuitivos** para cada componente
- 📝 **Campos de descripción dinámicos** que aparecen solo cuando hay problemas
- 💾 **Exportación a JSON** con timestamp y resumen
- ✨ **Validación completa** del formulario
- 🎨 **Interfaz responsive** y fácil de usar

## 🚀 Instalación y Uso

### Requisitos
- Python 3.13+
- Dependencias ya instaladas con uv

### Ejecutar la aplicación

```bash
# Opción 1: Ejecutar directamente
uv run python equipment_check_simple.py

# Opción 2: Usar el launcher
uv run python run_equipment_check.py
```

## 🎯 Funcionalidades

### **Componentes a Verificar**
1. **🖥️ Pantalla** - Estado del monitor
2. **⌨️ Teclado** - Funcionamiento del teclado
3. **🖱️ Ratón** - Estado del ratón/trackpad

### **Estados Disponibles**
- ✅ **Correcto** - El componente funciona perfectamente
- ❌ **Defectuoso** - El componente tiene problemas

### **Campos Dinámicos**
- Al seleccionar "Defectuoso", aparece automáticamente un campo de texto
- Permite describir detalladamente el problema encontrado
- Incluye texto de ejemplo para guiar al usuario

## 📄 Formato del JSON Generado

```json
{
  "timestamp": "2025-10-23T08:15:30.123456",
  "usuario": "usuario_actual",
  "verificacion_equipos": {
    "pantalla": {
      "estado": "correcto",
      "problema": null
    },
    "teclado": {
      "estado": "defectuoso",
      "problema": "Algunas teclas no responden correctamente"
    },
    "raton": {
      "estado": "correcto",
      "problema": null
    }
  },
  "resumen": {
    "total_componentes": 3,
    "componentes_correctos": 2,
    "componentes_defectuosos": 1,
    "equipo_operativo": false
  }
}
```

## 🔧 Características Técnicas

### **Validación del Formulario**
- Verifica que todos los componentes tengan estado seleccionado
- Requiere descripción obligatoria para componentes defectuosos
- Muestra mensajes de error específicos

### **Interfaz de Usuario**
- **Placeholders inteligentes** en campos de texto
- **Botones de acción** (Limpiar y Enviar)
- **Ventana de resultado** con resumen del estado
- **Centrado automático** de ventanas

### **Gestión de Archivos**
- Nombres de archivo con timestamp: `verificacion_equipos_YYYYMMDD_HHMMSS.json`
- Codificación UTF-8 para caracteres especiales
- Formato JSON indentado para legibilidad

## 🎨 Interfaz de Usuario

### **Pantalla Principal**
- Título y subtítulo informativos
- Secciones organizadas por componente
- Radiobuttons para selección de estado
- Campos de descripción que aparecen dinámicamente

### **Ventana de Resultado**
- Confirmación de envío exitoso
- Resumen del estado del equipo
- Visualización del JSON generado
- Opciones para nueva verificación o cerrar

## 🛠️ Personalización

### **Modificar Componentes**
Para añadir más componentes, edita la función `create_widgets()` y añade:

```python
self.nuevo_componente_estado = tk.StringVar(value="")
self.create_component_section(main_frame, "🔧 Nuevo Componente", self.nuevo_componente_estado, "nuevo_componente")
```

### **Cambiar Estilos**
Los colores y fuentes se pueden modificar en las funciones `create_widgets()` y `create_component_section()`.

### **Personalizar JSON**
Modifica la función `generate_json_report()` para añadir campos adicionales como:
- Información del usuario
- Ubicación del equipo
- Número de serie
- Fecha de última revisión

## 📊 Casos de Uso

### **Oficinas Corporativas**
- Control diario del estado de equipos
- Reportes de incidencias
- Mantenimiento preventivo

### **Centros de Trabajo**
- Verificación antes de turnos
- Documentación de problemas
- Seguimiento de reparaciones

### **Laboratorios**
- Control de equipos críticos
- Trazabilidad de fallos
- Reportes de calidad

## 🔍 Solución de Problemas

### **La aplicación no inicia**
```bash
# Verificar dependencias
uv pip list

# Reinstalar si es necesario
uv sync --reinstall
```

### **Error al guardar JSON**
- Verificar permisos de escritura en el directorio
- Comprobar espacio disponible en disco

### **Problemas de interfaz**
- Verificar que tkinter esté instalado correctamente
- Probar con diferentes temas de sistema

## 📝 Notas de Desarrollo

- **Versión actual**: 1.0
- **Compatibilidad**: Python 3.13+, multiplataforma
- **Dependencias**: tkinter (incluido en Python)
- **Arquitectura**: Aplicación de escritorio standalone

---

**¡Aplicación lista para usar!** 🎉
