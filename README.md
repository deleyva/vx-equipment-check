# Comprobación de PC Vitalinux

Aplicación de escritorio para verificar el estado de equipos de trabajo en VitaLinux, desarrollada con **Tauri** (Rust + Web).

## Características

- Formulario intuitivo de verificación de componentes
- Exportación automática de informes en formato JSON
- Diseño responsive adaptado a cualquier pantalla
- Rendimiento nativo gracias a Tauri
- Autostart al inicio de sesión en VitaLinux

## Componentes Verificables

- **Pantalla** (Obligatorio)
- **Teclado** (Obligatorio)
- **Ratón** (Opcional)
- **Batería** (Opcional)
- **Otros** (Opcional)

## Instalación en VitaLinux/Ubuntu

Descarga el paquete `.deb` desde la [página de Releases](https://github.com/deleyva/vx-dga-pc-check-form/releases/latest) e instálalo:

```bash
sudo dpkg -i vx-dga-pc-check-form_<VERSION>_amd64.deb
sudo apt install -f  # Instalar dependencias si es necesario
```

La aplicación se iniciará automáticamente al hacer login gracias al fichero `.desktop` instalado en `/etc/xdg/autostart/`.

### Dependencias del Sistema

```bash
sudo apt install libwebkit2gtk-4.0-37 libgtk-3-0
```

## Releases automáticos (CI/CD)

El proyecto usa GitHub Actions para generar releases automáticamente:

1. Actualizar versión en `package.json` y `src-tauri/tauri.conf.json`
2. Crear y subir tag:
   ```bash
   git tag v1.0.11
   git push origin v1.0.11
   ```
3. GitHub Actions construye el `.deb` y crea el release

## Desarrollo

```bash
# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev

# Construir para producción
npm run build
```

## Estructura del JSON generado

```json
{
  "timestamp": "2024-11-08T10:30:00.000Z",
  "empresa": "VITALINUX",
  "tipo_verificacion": "equipos_escritorio",
  "verificacion_equipos": {
    "pantalla": {
      "estado": "correcto|defectuoso",
      "problema": "descripción del problema",
      "obligatorio": true
    }
  },
  "resumen": {
    "total_componentes": 5,
    "componentes_correctos": 4,
    "componentes_defectuosos": 1,
    "equipo_operativo": false,
    "requiere_atencion": true
  }
}
```

## Configuración de la API

### Variable de Entorno VX_API_URL

Para un usuario concreto:

```bash
VX_API_URL="http://192.168.1.105:3001/v1/report" vx-dga-pc-check-form
```

Para configurarlo de forma permanente para **todos los usuarios del sistema**:

```bash
# Crear fichero de entorno global
sudo tee /etc/environment.d/vx-dga-pc-check-form.conf << 'EOF'
VX_API_URL="http://192.168.1.105:3001/v1/report"
EOF
```

> Los usuarios necesitan cerrar sesión y volver a entrar para que surta efecto.

Alternativa con `/etc/environment` (compatible con sistemas sin `environment.d`):

```bash
# Añadir al final de /etc/environment
echo 'VX_API_URL="http://192.168.1.105:3001/v1/report"' | sudo tee -a /etc/environment
```

### Modo Dry-Run (Testing)

```bash
vx-dga-pc-check-form --dry-run
```

## Comandos del Sistema

```bash
# Obtener usuario
migrasfree-cid

# Obtener CID
vx-usuario-grafico
```
