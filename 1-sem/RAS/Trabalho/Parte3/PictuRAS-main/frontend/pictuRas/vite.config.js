import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  // Base name of your app
  base: "/", // Replace this with the subdirectory path if needed
})
