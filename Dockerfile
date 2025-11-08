# Dockerfile para construir VITALINUX Equipment Check en Linux
FROM ubuntu:24.04

# Evitar prompts interactivos durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    build-essential \
    libssl-dev \
    libgtk-3-dev \
    libwebkit2gtk-4.1-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev \
    libsoup-3.0-dev \
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
COPY src-tauri/ ./src-tauri/
COPY vite.config.js ./

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
