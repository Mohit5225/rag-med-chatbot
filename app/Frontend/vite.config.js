 // filepath: c:\Users\mohit\Desktop\python\MEDICAL RAG CHATBOT\medical_rag_chatbot\app\Frontend\vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwind from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  plugins: [react(), tailwind()],
  resolve: {
    alias: {
      '@components': path.resolve(__dirname, './src/components'),
      '@common': path.resolve(__dirname, './src/common'),
      '@config': path.resolve(__dirname, './src/config')
    }
  }
})