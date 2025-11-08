import { defineConfig } from 'vite'

export default defineConfig({
  // Configuración para desarrollo
  server: {
    port: 3000,
    strictPort: true,
  },
  
  // Configuración para build
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: 'index.html'
      }
    }
  },
  
  // Configuración base
  base: './',
  
  // Optimizaciones
  optimizeDeps: {
    exclude: ['@tauri-apps/api']
  }
})
