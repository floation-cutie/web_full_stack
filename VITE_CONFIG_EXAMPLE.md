# GoodServices Frontend - Vite Configuration Guide

## vite.config.js

Create file `frontend/vite.config.js`:

```javascript
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig(({ mode }) => {
  // Load environment variables for the current mode
  const env = loadEnv(mode, process.cwd(), '')

  return {
    // ===========================================================================
    // PLUGINS
    // ===========================================================================
    plugins: [
      vue({
        // Vue 3 template compilation options
        template: {
          compilerOptions: {
            isCustomElement: (tag) => tag.includes('-')
          }
        }
      })
    ],

    // ===========================================================================
    // ENVIRONMENT VARIABLES
    // ===========================================================================
    define: {
      __APP_VERSION__: JSON.stringify(env.VITE_APP_VERSION || '1.0.0'),
      __APP_ENV__: JSON.stringify(env.VITE_ENVIRONMENT || 'development')
    },

    // ===========================================================================
    // RESOLVE ALIASES
    // ===========================================================================
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
        '@components': path.resolve(__dirname, './src/components'),
        '@views': path.resolve(__dirname, './src/views'),
        '@stores': path.resolve(__dirname, './src/stores'),
        '@api': path.resolve(__dirname, './src/api'),
        '@utils': path.resolve(__dirname, './src/utils'),
        '@assets': path.resolve(__dirname, './src/assets')
      }
    },

    // ===========================================================================
    // DEVELOPMENT SERVER
    // ===========================================================================
    server: {
      // Server port
      port: env.VITE_PORT || 5173,

      // Auto-open browser
      open: true,

      // Host binding (0.0.0.0 for Docker)
      host: '0.0.0.0',

      // Hot module replacement
      hmr: {
        host: 'localhost',
        port: 5173
      },

      // Proxy API requests to backend
      proxy: {
        '/api': {
          target: env.VITE_API_BASE_URL || 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path,
          // Log proxy requests
          logLevel: 'info'
        }
      },

      // Watch options
      watch: {
        usePolling: false,
        interval: 100
      }
    },

    // ===========================================================================
    // BUILD OPTIONS
    // ===========================================================================
    build: {
      // Output directory
      outDir: 'dist',

      // Asset directory
      assetsDir: 'assets',

      // Source map in production
      sourcemap: mode === 'development',

      // Minify CSS/JS
      minify: mode === 'production' ? 'terser' : false,

      // Terser options
      terserOptions: {
        compress: {
          drop_console: mode === 'production'
        }
      },

      // Chunk size warnings
      chunkSizeWarningLimit: 1000,

      // Rollup options
      rollupOptions: {
        output: {
          // Asset naming
          assetFileNames: 'assets/[name]-[hash][extname]',

          // Chunk naming
          chunkFileNames: 'assets/[name]-[hash].js',

          // Entry file naming
          entryFileNames: 'assets/[name]-[hash].js',

          // Manual chunks for better caching
          manualChunks: {
            'vendor-vue': ['vue', 'vue-router', 'pinia'],
            'vendor-ui': ['element-plus'],
            'vendor-echarts': ['echarts'],
            'vendor-axios': ['axios']
          }
        }
      },

      // CommonJS options
      commonjsOptions: {
        transformMixedEsModules: true
      }
    },

    // ===========================================================================
    // PREVIEW OPTIONS (for production preview)
    // ===========================================================================
    preview: {
      port: 4173,
      open: true,
      host: '0.0.0.0'
    },

    // ===========================================================================
    // CSS OPTIONS
    // ===========================================================================
    css: {
      postcss: './postcss.config.js',
      preprocessorOptions: {
        scss: {
          additionalData: '@import "@/assets/styles/variables.scss";'
        }
      }
    },

    // ===========================================================================
    # OPTIMIZATION
    // ===========================================================================
    optimizeDeps: {
      include: [
        'vue',
        'vue-router',
        'pinia',
        'axios',
        'element-plus',
        'echarts'
      ],
      exclude: ['node_modules']
    },

    // ===========================================================================
    // JSON OPTIONS
    // ===========================================================================
    json: {
      namedExports: true,
      stringify: true
    }
  }
})
```

## postcss.config.js

Create file `frontend/postcss.config.js`:

```javascript
export default {
  plugins: {
    autoprefixer: {},
    'postcss-preset-env': {
      stage: 3
    }
  }
}
```

## .browserslistrc

Create file `frontend/.browserslistrc` for autoprefixer:

```
> 1%
last 2 versions
not dead
not op_mini all
```

## vite.config.ts (TypeScript Version)

If using TypeScript, create `frontend/vite.config.ts`:

```typescript
import { defineConfig, loadEnv, UserConfig, ConfigEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig(({ mode }: ConfigEnv): UserConfig => {
  const env = loadEnv(mode, process.cwd(), '')

  return {
    plugins: [vue()],

    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src')
      }
    },

    server: {
      port: (env.VITE_PORT as unknown as number) || 5173,
      open: true,
      proxy: {
        '/api': {
          target: env.VITE_API_BASE_URL || 'http://localhost:8000',
          changeOrigin: true
        }
      }
    },

    build: {
      outDir: 'dist',
      sourcemap: mode === 'development',
      minify: 'terser'
    }
  }
})
```

## Environment-Based Configuration

### vite.config.dev.js (for development)

```javascript
import { mergeConfig } from 'vite'
import config from './vite.config.js'

export default mergeConfig(config, {
  define: {
    __DEV__: true
  },
  server: {
    middlewareMode: false,
    hmr: true
  }
})
```

### vite.config.prod.js (for production)

```javascript
import { mergeConfig } from 'vite'
import config from './vite.config.js'

export default mergeConfig(config, {
  define: {
    __DEV__: false
  },
  build: {
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    }
  }
})
```

## Usage Examples

### 1. Access Environment Variables in Vue Component

```vue
<template>
  <div>
    <h1>{{ appTitle }}</h1>
    <p v-if="isDevelopment">Development Mode</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const appTitle = computed(() => import.meta.env.VITE_APP_TITLE)
const isDevelopment = computed(() => import.meta.env.VITE_ENVIRONMENT === 'development')
</script>
```

### 2. Conditional API Base URL

```javascript
// src/api/index.js
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: import.meta.env.VITE_REQUEST_TIMEOUT || 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})
```

### 3. Feature Flags in Store

```javascript
// src/stores/config.js
import { defineStore } from 'pinia'

export const useConfigStore = defineStore('config', {
  state: () => ({
    features: {
      statistics: import.meta.env.VITE_ENABLE_STATISTICS === 'true',
      fileUpload: import.meta.env.VITE_ENABLE_FILE_UPLOAD === 'true',
      registration: import.meta.env.VITE_ENABLE_REGISTRATION === 'true'
    }
  })
})
```

## Development Workflow

```bash
# Install dependencies
npm install

# Start development server (hot reload)
npm run dev

# Build for production
npm run build

# Preview production build locally
npm run preview

# Run linting
npm run lint
```

## Docker Build Example

```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

ARG VITE_API_BASE_URL=http://localhost:8000
ARG VITE_ENVIRONMENT=production

ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_ENVIRONMENT=$VITE_ENVIRONMENT

RUN npm run build

# Serve stage
FROM node:18-alpine

WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app/dist ./dist

EXPOSE 5173

CMD ["serve", "-s", "dist", "-l", "5173"]
```

## Performance Optimization Tips

1. **Code Splitting**: Manually chunk large libraries
2. **Lazy Loading**: Use Vue Router lazy loading for routes
3. **Image Optimization**: Use WebP with fallbacks
4. **CSS Extraction**: Extract CSS to separate files in production
5. **Compression**: Enable gzip/brotli compression on server

## Common Issues & Solutions

### Issue: Environment variables not loading
- Ensure variable name starts with `VITE_`
- Restart dev server after changing .env file
- Check .env file is in project root

### Issue: Proxy not working
- Verify `VITE_API_BASE_URL` is correct
- Check backend server is running
- Look at browser console for proxy errors

### Issue: Hot reload not working
- Check HMR configuration in vite.config.js
- Restart dev server
- Clear browser cache
