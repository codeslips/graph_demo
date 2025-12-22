import { defineConfig, loadEnv, type ConfigEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig(({ mode }: ConfigEnv) => {
  // Load env file from project root
  const env = loadEnv(mode, fileURLToPath(new URL('..', import.meta.url)), '')

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    server: {
      host: '0.0.0.0',
      port: 5173,
      allowedHosts: env.ALLOWED_HOSTS 
        ? env.ALLOWED_HOSTS.split(',').map(h => h.trim()) 
        : ['10.101.102.105'],
      proxy: {
        '/api': {
          target: 'http://backend:8000',
          changeOrigin: true
        }
      }
    }
  }
})

