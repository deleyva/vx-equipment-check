// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::Command;
#[cfg(debug_assertions)]
use tauri::Manager;

#[tauri::command]
fn submit_form(app_handle: tauri::AppHandle, mut data: serde_json::Value) {
    // 1. Obtener migrasfree-cid
    // Intentamos ejecutar el comando. Si falla (ej. en Mac), usamos un valor mock.
    let cid = match Command::new("migrasfree-cid").output() {
        Ok(output) => String::from_utf8_lossy(&output.stdout).trim().to_string(),
        Err(_) => "MOCK_CID_12345".to_string(), 
    };

    // 2. Obtener vx-usuario-grafico
    let user_grafico = match Command::new("vx-usuario-grafico").output() {
        Ok(output) => String::from_utf8_lossy(&output.stdout).trim().to_string(),
        Err(_) => "MOCK_USER_DELEYVA".to_string(),
    };

    // 3. Insertar en el JSON recibido
    if let Some(obj) = data.as_object_mut() {
        obj.insert("migrasfree_cid".to_string(), serde_json::json!(cid));
        obj.insert("usuario_grafico".to_string(), serde_json::json!(user_grafico));
    }

    // 4. Construir string del JSON final
    let json_string = serde_json::to_string(&data).unwrap_or("{}".to_string());

    // 5. Imprimir comando CURL a stdout
    // La URL es un placeholder por ahora.
    println!("curl -X POST https://api.ejemplo.vitalinux/v1/report \\
              -H 'Content-Type: application/json' \\
              -d '{}'", json_string);

    // 6. Cerrar la aplicación
    app_handle.exit(0);
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![submit_form])
        .setup(|app| {
            #[cfg(debug_assertions)] // only include this code on debug builds
            {
                let window = app.get_window("main").unwrap();
                window.open_devtools();
            }
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
