import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  root: resolve(__dirname, 'main/webapp/static'),
  build: {
    outDir: resolve(__dirname, 'main/webapp/static/dist'),
    emptyOutDir: true,
    rollupOptions: {
      input: resolve(__dirname, 'main/webapp/static/index.html')
    }
  },
  server: {
    port: 3000
  }
});