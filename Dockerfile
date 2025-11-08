# Dockerfile para construir VITALINUX Equipment Check en Linux
FROM ubuntu:20.04

# Evitar prompts interactivos durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    build-essential \
    libssl-dev \
    libgtk-3-dev \
    libwebkit2gtk-4.0-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Instalar Node.js 18 LTS
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Instalar Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Instalar Tauri CLI
RUN npm install -g @tauri-apps/cli@1.5.14

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de configuración
COPY package*.json ./
COPY vite.config.js ./

# Copiar src-tauri excluyendo target/
COPY src-tauri/Cargo.toml ./src-tauri/
COPY src-tauri/Cargo.lock ./src-tauri/
COPY src-tauri/tauri.conf.json ./src-tauri/
COPY src-tauri/build.rs ./src-tauri/
COPY src-tauri/src/ ./src-tauri/src/
COPY src-tauri/icons/ ./src-tauri/icons/

# Instalar dependencias de Node.js
RUN npm ci

# Copiar archivos fuente
COPY index.html styles.css script.js vitalinux-logo.png ./

# Crear directorio dist y copiar archivos
RUN mkdir -p dist && \
    cp index.html styles.css script.js vitalinux-logo.png dist/

# Construir la aplicación
RUN tauri build

# Crear directorio de salida
RUN mkdir -p /output && \
    cp -r src-tauri/target/release/bundle/* /output/

# Comando por defecto
CMD ["ls", "-la", "/output"]
