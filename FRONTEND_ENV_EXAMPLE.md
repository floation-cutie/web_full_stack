# GoodServices Frontend Environment Configuration

## Frontend .env.example

Create a file named `.env.example` in the `frontend/` directory:

```env
# =============================================================================
# GoodServices Frontend Environment Configuration
# =============================================================================
# Copy this file to .env.development and .env.production
# Frontend uses Vite for environment variable loading
# =============================================================================

# =============================================================================
# API CONFIGURATION
# =============================================================================
# Backend API base URL (used by Axios)
VITE_API_BASE_URL=http://localhost:8000

# =============================================================================
# APPLICATION SETTINGS
# =============================================================================
# Environment type: development, testing, production
VITE_ENVIRONMENT=development

# Application title (shown in browser tab)
VITE_APP_TITLE=GoodServices

# Application version
VITE_APP_VERSION=1.0.0

# =============================================================================
# DEVELOPMENT SETTINGS (dev only)
# =============================================================================
# Enable development debugging tools
VITE_DEBUG=true

# Source map generation (enables browser debugging)
VITE_SOURCEMAP=true

# API request timeout (in milliseconds)
VITE_REQUEST_TIMEOUT=30000

# =============================================================================
# FEATURE FLAGS
# =============================================================================
# Enable user registration
VITE_ENABLE_REGISTRATION=true

# Enable admin panel link
VITE_ENABLE_ADMIN_PANEL=true

# Enable statistics module
VITE_ENABLE_STATISTICS=true

# Enable file upload feature
VITE_ENABLE_FILE_UPLOAD=true

# =============================================================================
# UI CONFIGURATION
# =============================================================================
# Default items per page for pagination
VITE_PAGINATION_PAGE_SIZE=10

# Show debug info in console
VITE_SHOW_DEBUG_INFO=false

# =============================================================================
# ANALYTICS (Optional)
# =============================================================================
# Google Analytics tracking ID
VITE_GA_TRACKING_ID=

# =============================================================================
# FEATURE TOGGLES
# =============================================================================
# Enable beta features
VITE_ENABLE_BETA_FEATURES=false

# Enable dark mode (user can override in settings)
VITE_ENABLE_DARK_MODE=false
```

## Environment-Specific Files

### .env.development

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_ENVIRONMENT=development
VITE_APP_TITLE=GoodServices (Dev)
VITE_DEBUG=true
VITE_SOURCEMAP=true
VITE_REQUEST_TIMEOUT=30000
VITE_ENABLE_REGISTRATION=true
VITE_ENABLE_ADMIN_PANEL=true
VITE_ENABLE_STATISTICS=true
VITE_ENABLE_FILE_UPLOAD=true
VITE_PAGINATION_PAGE_SIZE=10
VITE_SHOW_DEBUG_INFO=true
```

### .env.production

```env
VITE_API_BASE_URL=https://api.goodservices.com
VITE_ENVIRONMENT=production
VITE_APP_TITLE=GoodServices
VITE_DEBUG=false
VITE_SOURCEMAP=false
VITE_REQUEST_TIMEOUT=30000
VITE_ENABLE_REGISTRATION=true
VITE_ENABLE_ADMIN_PANEL=true
VITE_ENABLE_STATISTICS=true
VITE_ENABLE_FILE_UPLOAD=true
VITE_PAGINATION_PAGE_SIZE=10
VITE_SHOW_DEBUG_INFO=false
```

## Usage in Frontend Code

### In JavaScript/Vue files:

```javascript
// Accessing environment variables in Vue components
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL
const isProduction = import.meta.env.VITE_ENVIRONMENT === 'production'
const enableStats = import.meta.env.VITE_ENABLE_STATISTICS

// In axios configuration
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: import.meta.env.VITE_REQUEST_TIMEOUT
})

export default api
```

### In vite.config.js:

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { loadEnv } from 'vite'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd())

  return {
    plugins: [vue()],
    define: {
      __APP_ENV__: env.VITE_ENVIRONMENT
    },
    server: {
      port: 5173,
      proxy: {
        '/api': {
          target: env.VITE_API_BASE_URL,
          changeOrigin: true
        }
      }
    }
  }
})
```

## Important Notes

1. **Naming Convention**: All frontend environment variables MUST start with `VITE_` prefix
2. **Security**: Do NOT store sensitive secrets in frontend environment variables (they are visible in browser)
3. **Build Time**: Environment variables are embedded during build time, not runtime
4. **Reload**: After changing .env file, restart the dev server
5. **Production**: Use CI/CD to inject environment variables during deployment

## Environment Variable Validation

Frontend should validate critical environment variables on app initialization:

```javascript
// src/utils/config.js
export function validateEnv() {
  const required = ['VITE_API_BASE_URL', 'VITE_ENVIRONMENT']

  for (const key of required) {
    if (!import.meta.env[key]) {
      console.error(`Missing required env var: ${key}`)
      throw new Error(`Configuration error: ${key} not set`)
    }
  }
}
```

## Running Vite with Specific Environment

```bash
# Development
npm run dev          # Uses .env.development

# Production build
npm run build        # Uses .env.production

# Preview production build
npm run preview

# Specify custom environment file
npm run dev -- --mode=staging  # Uses .env.staging
```

## Docker Frontend Configuration

When using Docker, pass environment variables during build:

```dockerfile
ARG VITE_API_BASE_URL=http://localhost:8000
ARG VITE_ENVIRONMENT=production

RUN npm run build
```

Or in docker-compose.yml:

```yaml
services:
  frontend:
    environment:
      - VITE_API_BASE_URL=http://backend:8000
      - VITE_ENVIRONMENT=production
```
