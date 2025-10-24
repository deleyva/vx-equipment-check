# 🏢 MIGAS - Aplicación de Verificación de Equipos

**Versión Estilizada con Paleta Corporativa**

Una aplicación de escritorio moderna con GUI estilizada usando la paleta de colores corporativa de Migas (naranjas y verdes) para verificar el estado de equipos de trabajo.

## 🎨 Diseño y Estilo

### **Paleta de Colores Migas**
- **Naranja Primario**: `#FF6B35` - Botones principales y elementos destacados
- **Naranja Secundario**: `#FF8C42` - Estados hover y efectos
- **Verde Primario**: `#4CAF50` - Estados correctos y confirmaciones
- **Verde Secundario**: `#2E7D32` - Títulos y elementos de marca
- **Grises**: `#f8f9fa`, `#e9ecef`, `#495057` - Fondos y textos

### **Elementos de Diseño**
- ✅ **Header corporativo** con logo y branding Migas
- 🎨 **Cards estilizadas** para cada componente
- 🔘 **Radiobuttons con colores** (verde para correcto, rojo para defectuoso)
- 📝 **Campos de texto** con bordes naranjas y efectos hover
- 🔲 **Botones estilizados** con la paleta corporativa
- 📊 **Ventana de resultado** con indicadores visuales de estado

## 🚀 Instalación y Uso

### **Ejecutar la Aplicación Estilizada**

```bash
# Opción 1: Ejecutar directamente
uv run python equipment_check_styled.py

# Opción 2: Usar el launcher corporativo
uv run python run_migas_app.py
```

## 📋 Características Mejoradas

### **🎯 Interfaz Corporativa**
- **Branding Migas** integrado en toda la aplicación
- **Colores consistentes** con la identidad visual
- **Tipografías** optimizadas para legibilidad
- **Espaciado** y padding profesional

### **✨ Experiencia de Usuario**
- **Placeholders específicos** para cada tipo de componente
- **Validación visual** con colores de estado
- **Transiciones suaves** entre estados
- **Feedback inmediato** en todas las acciones

### **📊 Reporte Mejorado**
- **Metadatos corporativos** (empresa, tipo de verificación)
- **Campo adicional** `requiere_atencion` en el resumen
- **Nombres de archivo** con prefijo "migas_"
- **Estructura JSON** más completa

## 🎮 Funcionalidades

### **Componentes a Verificar**
1. **🖥️ Pantalla** - Monitor y display
2. **⌨️ Teclado** - Teclado físico o virtual
3. **🖱️ Ratón** - Mouse, trackpad o dispositivo de puntero

### **Estados con Estilo**
- **✅ Funcionamiento Correcto** (Verde Migas)
- **❌ Presenta Defectos** (Rojo de alerta)

### **Campos Dinámicos Mejorados**
- **Separadores visuales** cuando aparecen los campos
- **Placeholders específicos** por tipo de componente:
  - **Pantalla**: "La pantalla parpadea constantemente, hay líneas verticales..."
  - **Teclado**: "Algunas teclas no responden, la tecla espacio está atascada..."
  - **Ratón**: "El botón izquierdo no funciona bien, la rueda de scroll está bloqueada..."

## 📄 JSON Corporativo Generado

```json
{
  "timestamp": "2025-10-23T09:30:15.123456",
  "empresa": "MIGAS",
  "tipo_verificacion": "equipos_escritorio",
  "usuario": "usuario_actual",
  "verificacion_equipos": {
    "pantalla": {
      "estado": "correcto",
      "problema": null
    },
    "teclado": {
      "estado": "defectuoso", 
      "problema": "Descripción detallada del problema..."
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
    "equipo_operativo": false,
    "requiere_atencion": true
  }
}
```

## 🎨 Elementos Visuales

### **Ventana Principal**
- **Header Migas** con título corporativo
- **Instrucciones claras** con tipografía legible
- **Cards de componentes** con bordes y sombras sutiles
- **Botones de acción** con colores corporativos

### **Ventana de Resultado**
- **Estado visual del equipo**:
  - 🟢 **Verde**: "EQUIPO OPERATIVO"
  - 🟠 **Naranja**: "REQUIERE ATENCIÓN"
- **Información del archivo** destacada
- **JSON formateado** con sintaxis highlighting
- **Botones de acción** estilizados

## 🔧 Personalización Corporativa

### **Cambiar Colores**
Modifica la paleta en `self.colors`:

```python
self.colors = {
    'primary_orange': '#FF6B35',    # Tu color primario
    'secondary_orange': '#FF8C42',  # Color secundario
    'primary_green': '#4CAF50',     # Color de éxito
    'secondary_green': '#2E7D32',   # Color de marca
    # ... más colores
}
```

### **Personalizar Branding**
- Cambiar "MIGAS" por tu empresa en `create_header()`
- Modificar el prefijo de archivos en `submit_form()`
- Actualizar metadatos en `generate_json_report()`

## 📊 Casos de Uso Corporativos

### **Control de Calidad**
- Verificación diaria de equipos
- Reportes para mantenimiento
- Trazabilidad de incidencias

### **Gestión de IT**
- Inventario de estado de equipos
- Planificación de reemplazos
- Documentación de problemas

### **Auditorías**
- Reportes de estado para auditorías
- Evidencia de mantenimiento preventivo
- Historial de verificaciones

## 🎯 Mejoras Implementadas

### **Respecto a la Versión Básica**
- ✅ **Paleta corporativa** Migas integrada
- ✅ **Branding consistente** en toda la aplicación
- ✅ **Estilos profesionales** con ttk.Style personalizado
- ✅ **Placeholders específicos** por componente
- ✅ **Ventana de resultado** mejorada con indicadores visuales
- ✅ **JSON corporativo** con metadatos adicionales
- ✅ **Experiencia de usuario** optimizada

### **Elementos Técnicos**
- **Estilos TTK personalizados** para cada tipo de widget
- **Gestión de colores centralizada** en diccionario
- **Separadores visuales** y elementos de diseño
- **Contenedores con bordes** y efectos visuales
- **Tipografías consistentes** en toda la aplicación

---

**🏢 Aplicación corporativa Migas lista para producción!** 🎉
