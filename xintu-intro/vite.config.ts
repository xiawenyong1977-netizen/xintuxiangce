import path from 'path';
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, '.', '');
    return {
      server: {
        port: 3000,
        host: '0.0.0.0',
      },
      plugins: [react()],
      define: {
        'process.env.API_KEY': JSON.stringify(env.GEMINI_API_KEY),
        'process.env.GEMINI_API_KEY': JSON.stringify(env.GEMINI_API_KEY)
      },
      resolve: {
        alias: {
          '@': path.resolve(__dirname, '.'),
        }
      },
      // 构建输出到 website 目录
      build: {
        outDir: '../website',
        emptyOutDir: false, // 不清空 website 目录，只覆盖构建产物
        rollupOptions: {
          output: {
            // 将 React 应用的资源输出到 assets/react/ 目录
            assetFileNames: 'assets/react/[name]-[hash][extname]',
            chunkFileNames: 'assets/react/[name]-[hash].js',
            entryFileNames: 'assets/react/[name]-[hash].js',
          }
        }
      }
    };
});
