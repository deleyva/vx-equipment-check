# AGENTS.md - Contexto del Proyecto VITALINUX Equipment Check

## 📋 Información del Proyecto

**Nombre:** VITALINUX Equipment Check  
**Tipo:** Aplicación de escritorio para verificación de equipos  
**Tecnología:** Tauri (Rust + HTML/CSS/JavaScript)  
**Usuario:** deleyva (VITALINUX Team)  
**Repositorio:** vx-equipment-check  

## 🎯 Propósito de la Aplicación

Aplicación de escritorio moderna para verificar el estado de equipos de trabajo en VitaLinux (distribución educativa basada en Ubuntu). Permite a los usuarios documentar el estado de componentes de hardware y generar informes en formato JSON.

## 🏗️ Arquitectura Técnica

### Frontend
- **HTML5:** Estructura semántica con formularios accesibles
- **CSS3:** Diseño moderno con variables CSS, gradientes, animaciones y responsive design
- **JavaScript ES6+:** Lógica de aplicación con manejo de eventos, validación y APIs de Tauri

### Backend
- **Rust (Tauri):** Runtime nativo para máximo rendimiento
- **APIs habilitadas:** Dialog (save), FileSystem (writeTextFile), Shell (open)
- **Permisos:** Acceso a Desktop, Documents, Downloads, Home

### Build System
- **Vite:** Bundler y servidor de desarrollo
- **Tauri CLI:** Compilación y empaquetado multiplataforma
- **Scripts personalizados:** build-linux.sh para automatización en Linux

## 📊 Funcionalidad Principal

### Componentes Verificables
1. **🖥️ Pantalla** (Obligatorio)
2. **⌨️ Teclado** (Obligatorio)
3. **🖱️ Ratón** (Opcional)
4. **🔋 Batería** (Opcional)
5. **⚙️ Otros** (Opcional)

### Estados Posibles
- **Correcto:** Funcionamiento normal
- **Defectuoso:** Requiere descripción obligatoria del problema

### Validación
- Componentes obligatorios deben tener estado seleccionado
- Componentes defectuosos requieren descripción detallada
- Validación en tiempo real con feedback visual

### Exportación
- Formato JSON estructurado con timestamp
- Diálogo nativo para seleccionar ubicación de guardado
- Modal de resultado con resumen y JSON completo

## 🎨 Diseño Visual

### Paleta de Colores (Variables CSS)
```css
--primary-orange: #ff6b35    /* Color principal VITALINUX */
--primary-green: #28a745     /* Estados correctos */
--secondary-blue: #007bff    /* Elementos interactivos */
--danger-red: #dc3545       /* Estados defectuosos */
--light-gray: #f8f9fa       /* Fondos */
--medium-gray: #6c757d      /* Textos secundarios */
--dark-gray: #495057        /* Textos principales */
```

### Características UI/UX
- **Logo personalizado:** vitalinux-logo.png en header
- **Animaciones fluidas:** Transiciones CSS para mejor experiencia
- **Responsive design:** Adaptable a diferentes tamaños de pantalla
- **Scroll suave:** Implementación nativa sin problemas de compatibilidad
- **Feedback visual:** Estados hover, focus y validación en tiempo real

## 📁 Estructura de Archivos

```
vx-login-app/
├── 🎨 Frontend Core
│   ├── index.html                   # Interfaz principal
│   ├── styles.css                   # Estilos con variables CSS
│   ├── script.js                    # Lógica de aplicación
│   └── vitalinux-logo.png          # Logo personalizado
├── ⚙️ Configuración
│   ├── package.json                 # Dependencias Node.js
│   ├── vite.config.js              # Configuración Vite
│   └── src-tauri/
│       ├── tauri.conf.json         # Configuración Tauri
│       ├── Cargo.toml              # Dependencias Rust
│       ├── src/main.rs             # Backend Rust
│       └── icons/                  # Iconos aplicación
├── 🔧 Scripts y Herramientas
│   └── build-linux.sh              # Build automatizado Linux
├── 📖 Documentación
│   ├── README.md                   # Documentación completa
│   └── AGENTS.md                   # Este archivo
└── 🏗️ Build Output
    └── dist/                       # Archivos para desarrollo
```

## 🔧 Comandos Principales

### Desarrollo
```bash
npm install                    # Instalar dependencias
npm run dev                   # Servidor desarrollo con hot reload
tauri dev --verbose           # Desarrollo con logs detallados
```

### Producción
```bash
npm run build                 # Build multiplataforma
npm run build-deb            # Build específico Linux
./build-linux.sh            # Script automatizado Linux
```

### Mantenimiento
```bash
npm run clean                # Limpiar cache y builds
cp *.html *.css *.js *.png dist/  # Actualizar archivos desarrollo
```

## 📦 Distribución

### Formatos Generados
- **Linux:** .deb, .rpm, .AppImage
- **macOS:** .app, .dmg
- **Windows:** .msi, .exe

### Dependencias Sistema
- **Ubuntu/VitaLinux:** libwebkit2gtk-4.0-37, libgtk-3-0
- **Fedora/CentOS:** webkit2gtk3, gtk3

### Tamaños Aproximados
- **.deb/.rpm:** ~15-20 MB
- **.AppImage:** ~20-25 MB
- **.dmg/.msi:** ~15-20 MB

## 🔄 Flujo de Trabajo

### Desarrollo Típico
1. Modificar archivos frontend (HTML/CSS/JS)
2. Copiar a dist/: `cp index.html styles.css script.js vitalinux-logo.png dist/`
3. Probar con: `npm run dev`
4. Build final: `npm run build`

### Actualización de Versión
1. Actualizar version en `package.json`
2. Actualizar version en `src-tauri/tauri.conf.json`
3. Ejecutar build completo
4. Distribuir nuevos instaladores

## 🚨 Problemas Comunes y Soluciones

### Error: "tauri command not found"
```bash
npm install -g @tauri-apps/cli
```

### Error: "Rust not found"
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env
```

### Error: "failed to get cargo metadata"
- Verificar que Rust esté en PATH
- Ejecutar `source ~/.cargo/env`
- Reinstalar dependencias si es necesario

### Campos de descripción no aparecen
- Verificar IDs en HTML coinciden con JavaScript
- Comprobar event listeners en setupRadioListeners()
- Revisar función handleRadioChange()

### Modal de resultado no aparece
- Verificar APIs de Tauri están disponibles
- Comprobar función showResultModal()
- Revisar permisos de archivo en tauri.conf.json

## 📊 Estructura JSON de Salida

```json
{
  "timestamp": "ISO 8601 string",
  "empresa": "VITALINUX",
  "tipo_verificacion": "equipos_escritorio",
  "usuario": "usuario_actual",
  "verificacion_equipos": {
    "pantalla": {
      "estado": "correcto|defectuoso",
      "problema": "string|null",
      "obligatorio": true
    },
    "teclado": {
      "estado": "correcto|defectuoso", 
      "problema": "string|null",
      "obligatorio": true
    },
    "raton": {
      "estado": "correcto|defectuoso|no_verificado",
      "problema": "string|null", 
      "obligatorio": false
    },
    "bateria": {
      "estado": "correcto|defectuoso|no_verificado",
      "problema": "string|null",
      "obligatorio": false  
    },
    "otros": {
      "estado": "correcto|defectuoso|no_verificado",
      "problema": "string|null",
      "obligatorio": false
    }
  },
  "resumen": {
    "total_componentes": 5,
    "componentes_obligatorios": 2,
    "componentes_opcionales": 3,
    "componentes_verificados": "number",
    "componentes_correctos": "number", 
    "componentes_defectuosos": "number",
    "equipo_operativo": "boolean",
    "requiere_atencion": "boolean"
  }
}
```

## 🎯 Objetivos del Proyecto

### Funcionales
- ✅ Formulario intuitivo de verificación
- ✅ Validación robusta con feedback claro
- ✅ Exportación JSON estructurada
- ✅ Interfaz responsive y accesible

### Técnicos  
- ✅ Rendimiento nativo (Tauri)
- ✅ Compatibilidad multiplataforma
- ✅ Distribución automatizada
- ✅ Tamaño optimizado (~15MB)

### UX/UI
- ✅ Diseño moderno con animaciones
- ✅ Logo personalizado VITALINUX
- ✅ Scroll suave en todas las plataformas
- ✅ Feedback visual inmediato

## 🔮 Contexto Histórico

**Migración completada:** Este proyecto fue migrado exitosamente desde una implementación Python/tkinter que tenía problemas de compatibilidad entre macOS y VitaLinux. La nueva implementación con Tauri resuelve todos los problemas previos y ofrece mejor rendimiento, distribución más sencilla y experiencia de usuario superior.

**Archivos eliminados:** Se eliminaron todos los archivos relacionados con Python (vitalinux_equipment_check.py, run.py, pyproject.toml, etc.) para mantener el proyecto limpio y enfocado en la implementación Tauri.

## 🤝 Notas para Agentes

- **Siempre** copiar archivos a dist/ después de modificaciones: `cp index.html styles.css script.js vitalinux-logo.png dist/`
- **Mantener** consistencia en IDs entre HTML y JavaScript
- **Validar** que las APIs de Tauri estén disponibles antes de usarlas
- **Probar** funcionalidad completa después de cambios
- **Documentar** cualquier nueva funcionalidad en README.md
- **Respetar** la paleta de colores y diseño establecido
- **Considerar** compatibilidad con VitaLinux como prioridad
