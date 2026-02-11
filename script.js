// Importar APIs de Tauri de forma segura
let tauriAPI = null;
try {
    if (window.__TAURI__) {
        tauriAPI = {
            invoke: window.__TAURI__.tauri.invoke,
            save: window.__TAURI__.dialog.save,
            writeTextFile: window.__TAURI__.fs.writeTextFile
        };
    }
} catch (error) {
    console.log('Tauri APIs no disponibles, usando fallback');
}

// Estado de la aplicación
let formData = {
    pantalla: '',
    teclado: '',
    raton: '',
    bateria: '',
    otros: ''
};

let descriptions = {
    pantalla: '',
    teclado: '',
    raton: '',
    bateria: '',
    otros: ''
};

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    console.log('🚀 Iniciando aplicación VITALINUX...');
    
    // Configurar event listeners para radio buttons
    setupRadioListeners();
    
    // Configurar botones de acción
    setupActionButtons();
    
    // Configurar modal
    setupModal();
    
    console.log('✅ Aplicación inicializada correctamente');
}

function setupRadioListeners() {
    const components = ['pantalla', 'teclado', 'raton', 'bateria', 'otros'];
    
    components.forEach(component => {
        const radios = document.querySelectorAll(`input[name="${component}"]`);
        
        radios.forEach(radio => {
            radio.addEventListener('change', function() {
                handleRadioChange(component, this.value);
            });
        });
    });
}

function handleRadioChange(component, value) {
    console.log(`📝 ${component}: ${value}`);
    
    formData[component] = value;
    
    const descField = document.getElementById(`${component}-desc`);
    
    if (!descField) {
        console.error(`No se encontró el campo de descripción para ${component}`);
        return;
    }
    
    const textarea = descField.querySelector('textarea');
    
    if (value === 'defectuoso') {
        // Mostrar campo de descripción con animación
        descField.style.display = 'block';
        setTimeout(() => {
            textarea.focus();
        }, 100);
        
        // Añadir event listener para actualizar descripción
        if (!textarea.hasAttribute('data-listener-added')) {
            textarea.addEventListener('input', function() {
                descriptions[component] = this.value.trim();
            });
            textarea.setAttribute('data-listener-added', 'true');
        }
    } else {
        // Ocultar campo de descripción
        descField.style.display = 'none';
        textarea.value = '';
        descriptions[component] = '';
    }
}

function setupActionButtons() {
    const clearBtn = document.getElementById('clearBtn');
    const submitBtn = document.getElementById('submitBtn');
    const form = document.getElementById('equipmentForm');
    
    clearBtn.addEventListener('click', clearForm);
    form.addEventListener('submit', handleSubmit);
}

function clearForm() {
    console.log('🗑️ Limpiando formulario...');
    
    // Limpiar radio buttons
    const radios = document.querySelectorAll('input[type="radio"]');
    radios.forEach(radio => {
        radio.checked = false;
    });
    
    // Ocultar campos de descripción
    const descFields = document.querySelectorAll('.description-field');
    descFields.forEach(field => {
        field.style.display = 'none';
    });
    
    // Limpiar textareas
    const textareas = document.querySelectorAll('.description-textarea');
    textareas.forEach(textarea => {
        textarea.value = '';
    });
    
    // Resetear estado
    formData = {
        pantalla: '',
        teclado: '',
        raton: '',
        bateria: '',
        otros: ''
    };
    
    descriptions = {
        pantalla: '',
        teclado: '',
        raton: '',
        bateria: '',
        otros: ''
    };
    
    showNotification('✅ Formulario limpiado', 'Se han borrado todos los datos del formulario.', 'success');
}

function handleSubmit(event) {
    event.preventDefault();
    console.log('📤 Enviando formulario...');
    
    // Actualizar descripciones actuales
    updateDescriptions();
    
    // Validar formulario
    const errors = validateForm();
    
    if (errors.length > 0) {
        const errorMessage = 'Por favor, completa los siguientes campos:\n\n' + errors.join('\n');
        showNotification('❌ Formulario Incompleto', errorMessage, 'error');
        return;
    }
    
    // Generar y enviar reporte al backend
    submitFormToBackend();
}

async function submitFormToBackend() {
    try {
        console.log('📤 Enviando datos al sistema...');
        
        const report = generateJsonReport();
        
        if (tauriAPI && tauriAPI.invoke) {
            // Invocar comando Rust que:
            // 1. Ejecuta comandos de sistema (cid, usuario)
            // 2. Genera curl en stdout
            // 3. Cierra la aplicación
            await tauriAPI.invoke('submit_form', { data: report });
        } else {
            // Fallback para desarrollo en navegador
            console.warn('⚠️ Tauri API no disponible. JSON generado:');
            console.log(JSON.stringify(report, null, 2));
            showNotification('⚠️ Modo Navegador', 'Se ha generado el JSON en la consola (F12). En producción la app se cerraría.', 'info');
        }
        
    } catch (error) {
        console.error('❌ Error al enviar:', error);
        showNotification('❌ Error', `Error al procesar envío:\n${error.message}`, 'error');
    }
}

// Función obsoleta por ahora
// async function generateAndSaveReport() { ... }

function updateDescriptions() {
    const components = ['pantalla', 'teclado', 'raton', 'bateria', 'otros'];
    
    components.forEach(component => {
        const textarea = document.querySelector(`#${component}-desc textarea`);
        if (textarea && formData[component] === 'defectuoso') {
            descriptions[component] = textarea.value.trim();
        }
    });
}

function validateForm() {
    const errors = [];
    
    // Verificar componentes obligatorios
    if (!formData.pantalla) {
        errors.push('• Selecciona el estado de la pantalla (obligatorio)');
    }
    
    if (!formData.teclado) {
        errors.push('• Selecciona el estado del teclado (obligatorio)');
    }
    
    // Verificar descripciones para componentes defectuosos
    const components = ['pantalla', 'teclado', 'raton', 'bateria', 'otros'];
    const componentNames = {
        pantalla: 'pantalla',
        teclado: 'teclado',
        raton: 'ratón',
        bateria: 'batería',
        otros: 'sección "Otros"'
    };
    
    components.forEach(component => {
        if (formData[component] === 'defectuoso') {
            // Obtener el texto actual del textarea
            const textarea = document.querySelector(`#${component}-desc textarea`);
            const currentText = textarea ? textarea.value.trim() : '';
            
            if (!currentText) {
                errors.push(`• Describe el problema de la ${componentNames[component]} (obligatorio cuando hay defectos)`);
            } else {
                // Actualizar descriptions con el valor actual
                descriptions[component] = currentText;
            }
        }
    });
    
    return errors;
}

async function generateAndSaveReport() {
    try {
        console.log('📊 Generando reporte...');
        
        const report = generateJsonReport();
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
        const filename = `vitalinux_verificacion_equipos_${timestamp}.json`;
        
        if (tauriAPI && tauriAPI.save && tauriAPI.writeTextFile) {
            // Usar API de Tauri para guardar archivo
            const filePath = await tauriAPI.save({
                defaultPath: filename,
                filters: [{
                    name: 'JSON',
                    extensions: ['json']
                }]
            });
            
            if (filePath) {
                await tauriAPI.writeTextFile(filePath, JSON.stringify(report, null, 2));
                console.log('✅ Archivo guardado:', filePath);
                showResultModal(report, filename);
            }
        } else {
            // Fallback para navegador - descargar archivo
            const jsonString = JSON.stringify(report, null, 2);
            const blob = new Blob([jsonString], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            console.log('✅ Archivo descargado:', filename);
            showResultModal(report, filename);
        }
        
    } catch (error) {
        console.error('❌ Error al guardar:', error);
        showNotification('❌ Error', `Error al guardar el archivo:\n${error.message}`, 'error');
    }
}

function generateJsonReport() {
    const now = new Date();
    
    // Obtener estados válidos
    const estados = [
        formData.pantalla,
        formData.teclado,
        formData.raton || null,
        formData.bateria || null,
        formData.otros || null
    ];
    
    const estadosValidos = estados.filter(estado => estado);
    
    const report = {
        timestamp: now.toISOString(),
        verificacion_equipos: {
            pantalla: {
                estado: formData.pantalla,
                problema: formData.pantalla === 'defectuoso' ? descriptions.pantalla : null,
                obligatorio: true
            },
            teclado: {
                estado: formData.teclado,
                problema: formData.teclado === 'defectuoso' ? descriptions.teclado : null,
                obligatorio: true
            },
            raton: {
                estado: formData.raton || "no_verificado",
                problema: formData.raton === 'defectuoso' ? descriptions.raton : null,
                obligatorio: false
            },
            bateria: {
                estado: formData.bateria || "no_verificado",
                problema: formData.bateria === 'defectuoso' ? descriptions.bateria : null,
                obligatorio: false
            },
            otros: {
                estado: formData.otros || "no_verificado",
                problema: formData.otros === 'defectuoso' ? descriptions.otros : null,
                obligatorio: false
            }
        },
        resumen: {
            total_componentes: 5,
            componentes_obligatorios: 2,
            componentes_opcionales: 3,
            componentes_verificados: estadosValidos.length,
            componentes_correctos: estadosValidos.filter(estado => estado === "correcto").length,
            componentes_defectuosos: estadosValidos.filter(estado => estado === "defectuoso").length,
            equipo_operativo: estados.every(estado => estado === "correcto" || estado === "no_verificado" || estado === null),
            requiere_atencion: estadosValidos.some(estado => estado === "defectuoso")
        }
    };
    
    return report;
}

function showResultModal(report, filePath) {
    const modal = document.getElementById('resultModal');
    const fileName = document.getElementById('resultFileName');
    const status = document.getElementById('resultStatus');
    const summary = document.getElementById('resultSummary');
    const jsonOutput = document.getElementById('jsonOutput');
    
    // Actualizar contenido del modal
    fileName.textContent = `📁 Archivo guardado: ${filePath.split('/').pop()}`;
    
    const resumen = report.resumen;
    if (resumen.equipo_operativo) {
        status.innerHTML = '<div class="status-ok">🟢 EQUIPO OPERATIVO</div>';
    } else {
        status.innerHTML = '<div class="status-warning">🟠 REQUIERE ATENCIÓN</div>';
    }
    
    summary.textContent = `Componentes correctos: ${resumen.componentes_correctos}/${resumen.componentes_verificados} | Defectuosos: ${resumen.componentes_defectuosos}/${resumen.componentes_verificados}`;
    
    jsonOutput.textContent = JSON.stringify(report, null, 2);
    
    // Mostrar modal
    modal.style.display = 'flex';
}

function setupModal() {
    const modal = document.getElementById('resultModal');
    const newVerificationBtn = document.getElementById('newVerificationBtn');
    const closeModalBtn = document.getElementById('closeModalBtn');
    
    newVerificationBtn.addEventListener('click', function() {
        modal.style.display = 'none';
        clearForm();
    });
    
    closeModalBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    // Cerrar modal al hacer clic fuera
    modal.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}

function showNotification(title, message, type = 'info') {
    // Crear notificación personalizada
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <h4>${title}</h4>
            <p>${message}</p>
            <button class="notification-close">×</button>
        </div>
    `;
    
    // Estilos para la notificación
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        z-index: 2000;
        max-width: 400px;
        animation: slideInRight 0.3s ease;
    `;
    
    const content = notification.querySelector('.notification-content');
    content.style.cssText = `
        padding: 20px;
        border-left: 4px solid ${type === 'error' ? '#dc3545' : type === 'success' ? '#28a745' : '#007bff'};
    `;
    
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.style.cssText = `
        position: absolute;
        top: 10px;
        right: 15px;
        background: none;
        border: none;
        font-size: 20px;
        cursor: pointer;
        color: #666;
    `;
    
    document.body.appendChild(notification);
    
    // Auto-cerrar después de 5 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
    
    // Cerrar al hacer clic
    closeBtn.addEventListener('click', () => {
        notification.remove();
    });
}

// Agregar estilos CSS para las animaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .notification h4 {
        margin: 0 0 10px 0;
        font-size: 1.1rem;
    }
    
    .notification p {
        margin: 0;
        white-space: pre-line;
        color: #666;
    }
`;
document.head.appendChild(style);

console.log('🎯 Script cargado correctamente');
