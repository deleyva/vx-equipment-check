// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::Command;
use std::env;
#[cfg(debug_assertions)]
use tauri::Manager;

/// Check if --dry-run flag is passed
fn is_dry_run() -> bool {
    env::args().any(|arg| arg == "--dry-run")
}

/// Get API URL from environment variable or use default
fn get_api_url() -> String {
    env::var("VX_API_URL")
        .unwrap_or_else(|_| "http://172.16.0.249:3001/v1/report".to_string())
}

#[tauri::command]
fn submit_form(app_handle: tauri::AppHandle, mut data: serde_json::Value) {
    // 1. Obtener migasfree-cid
    let cid = match Command::new("/usr/bin/migasfree-cid").output() {
        Ok(output) => {
            let stdout = String::from_utf8_lossy(&output.stdout).trim().to_string();
            let stderr = String::from_utf8_lossy(&output.stderr).trim().to_string();
            println!("[DEBUG] /usr/bin/migasfree-cid exit={} stdout='{}' stderr='{}'", output.status, stdout, stderr);
            if !stdout.is_empty() {
                stdout
            } else if !stderr.is_empty() {
                stderr
            } else {
                String::new()
            }
        }
        Err(e) => {
            eprintln!("[ERROR] /usr/bin/migasfree-cid not found: {}", e);
            String::new()
        }
    };

    // 2. Obtener vx-usuario-grafico
    let user_grafico = match Command::new("vx-usuario-grafico").output() {
        Ok(output) => String::from_utf8_lossy(&output.stdout).trim().to_string(),
        Err(_) => "MOCK_USER_DELEYVA".to_string(),
    };

    // 3. Insertar en el JSON recibido
    if let Some(obj) = data.as_object_mut() {
        obj.insert("migasfree_cid".to_string(), serde_json::json!(cid));
        obj.insert("usuario_grafico".to_string(), serde_json::json!(user_grafico));
    }

    // 4. Get API URL and check dry-run mode
    let api_url = get_api_url();
    let dry_run = is_dry_run();

    if dry_run {
        // Dry-run mode: print curl command without sending
        let json_string = serde_json::to_string(&data).unwrap_or("{}".to_string());
        println!("[DRY-RUN] Would send to: {}", api_url);
        println!("curl -X POST {} \\
              -H 'Content-Type: application/json' \\
              -d '{}'", api_url, json_string);
    } else {
        // Production mode: send real HTTP POST
        println!("[DEBUG] Sending to: {}", api_url);
        println!("[DEBUG] Payload: {}", serde_json::to_string_pretty(&data).unwrap_or("{}".to_string()));

        let client = reqwest::blocking::Client::new();
        match client.post(&api_url)
            .json(&data)
            .send()
        {
            Ok(response) => {
                let status = response.status();
                if status.is_success() {
                    println!("[OK] Report sent successfully to {}", api_url);
                } else {
                    let body = response.text().unwrap_or_else(|_| "No body".to_string());
                    eprintln!("[ERROR] Server responded with status: {}", status);
                    eprintln!("[ERROR] Response body: {}", body);
                }
            }
            Err(e) => {
                eprintln!("[ERROR] Failed to send report: {}", e);
            }
        }
    }

    // 5. Cerrar la aplicación
    app_handle.exit(0);
}

fn main() {
    // DEBUG: Print API URL at startup
    let api_url = get_api_url();
    println!("[DEBUG] VX_API_URL = {}", api_url);

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
