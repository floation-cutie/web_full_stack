# GoodServices Frontend - package.json Configuration

## Complete package.json for Vue 3 + Vite Project

Create file `frontend/package.json`:

```json
{
  "name": "goodservices-frontend",
  "version": "1.0.0",
  "description": "GoodServices - Community Service Matching Platform Frontend",
  "type": "module",
  "author": "GoodServices Team",
  "license": "MIT",
  "homepage": "https://github.com/yourorg/goodservices",
  "repository": {
    "type": "git",
    "url": "https://github.com/yourorg/goodservices.git"
  },
  "bugs": {
    "url": "https://github.com/yourorg/goodservices/issues"
  },

  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "build:staging": "vite build --mode staging",
    "build:production": "vite build --mode production",
    "preview": "vite preview",
    "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs --fix --ignore-path .gitignore",
    "format": "prettier --write --ignore-path .gitignore",
    "type-check": "vue-tsc --noEmit -p tsconfig.app.json --composite false"
  },

  "dependencies": {
    "vue": "^3.3.13",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.6",
    "axios": "^1.6.5",
    "element-plus": "^2.4.4",
    "echarts": "^5.4.3",
    "@element-plus/icons-vue": "^2.1.0"
  },

  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.4",
    "vite": "^5.0.8",
    "vue-tsc": "^1.8.22",
    "@vue/compiler-sfc": "^3.3.13",
    "@types/node": "^20.10.6",
    "postcss": "^8.4.32",
    "postcss-preset-env": "^9.3.0",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.56.0",
    "@eslint/js": "^8.56.0",
    "eslint-plugin-vue": "^9.20.0",
    "prettier": "^3.1.1"
  },

  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  },

  "browserslist": [
    "> 1%",
    "last 2 versions",
    "not dead",
    "not op_mini all"
  ]
}
```

## Alternative: Minimal package.json

For a simpler setup without TypeScript support:

```json
{
  "name": "goodservices-frontend",
  "version": "1.0.0",
  "description": "GoodServices Frontend - Vue 3 + Vite",
  "type": "module",

  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext .vue,.js --fix"
  },

  "dependencies": {
    "vue": "^3.3.13",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.6",
    "axios": "^1.6.5",
    "element-plus": "^2.4.4",
    "echarts": "^5.4.3"
  },

  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.4",
    "vite": "^5.0.8",
    "eslint": "^8.56.0",
    "eslint-plugin-vue": "^9.20.0",
    "prettier": "^3.1.1"
  },

  "engines": {
    "node": ">=18.0.0"
  }
}
```

## Dependency Explanations

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **vue** | ^3.3.13 | Frontend framework (required) |
| **vue-router** | ^4.2.5 | SPA routing |
| **pinia** | ^2.1.6 | State management |
| **axios** | ^1.6.5 | HTTP client for API calls |
| **element-plus** | ^2.4.4 | UI component library |
| **echarts** | ^5.4.3 | Data visualization (statistics) |
| **@element-plus/icons-vue** | ^2.1.0 | Icon library |

### Dev Dependencies

| Package | Purpose |
|---------|---------|
| **@vitejs/plugin-vue** | Vue support for Vite |
| **vite** | Build tool and dev server |
| **eslint** | Code linting |
| **eslint-plugin-vue** | Vue-specific linting rules |
| **prettier** | Code formatting |
| **postcss** | CSS processing |
| **autoprefixer** | Add vendor prefixes |

## Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Or using npm ci for exact versions (production)
npm ci

# Install specific package
npm install package-name

# Install dev dependency
npm install --save-dev package-name

# Uninstall package
npm uninstall package-name

# Update all packages
npm update

# Check outdated packages
npm outdated
```

## Available Scripts

```bash
# Start development server
npm run dev
# Starts Vite dev server at http://localhost:5173

# Build for production
npm run build
# Creates optimized dist/ directory for deployment

# Build for staging environment
npm run build:staging
# Uses .env.staging configuration

# Preview production build locally
npm run preview
# Serves dist/ locally at http://localhost:4173

# Lint and fix code
npm run lint
# Fixes ESLint issues, formats Vue files

# Format code with Prettier
npm run format
# Formats all code files

# Type checking (if using TypeScript)
npm run type-check
# Validates TypeScript types without compiling
```

## Directory Structure

```
frontend/
├── src/
│   ├── components/        # Reusable Vue components
│   ├── views/            # Page components (with routing)
│   ├── stores/           # Pinia stores (state management)
│   ├── api/              # API client functions
│   ├── router/           # Vue Router configuration
│   ├── assets/           # Static assets (CSS, images, fonts)
│   │   ├── styles/       # Global CSS/SCSS files
│   │   └── images/       # Images
│   ├── utils/            # Utility functions
│   ├── App.vue           # Root component
│   └── main.js           # Entry point
├── public/               # Static files (copied as-is)
├── package.json          # Project metadata and dependencies
├── package-lock.json     # Locked dependency versions
├── vite.config.js        # Vite configuration
├── index.html            # HTML template
├── .env.development      # Development environment
├── .env.production       # Production environment
├── .eslintrc.js          # ESLint configuration
├── .prettierrc            # Prettier configuration
└── README.md             # Project readme
```

## Configuration Files

### .eslintrc.js

```javascript
module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true
  },
  extends: [
    'plugin:vue/vue3-recommended',
    'eslint:recommended'
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  rules: {
    'vue/multi-word-component-names': 'off',
    'vue/no-v-html': 'off'
  }
}
```

### .prettierrc

```json
{
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "semi": false,
  "singleQuote": true,
  "trailingComma": "es5",
  "bracketSpacing": true,
  "arrowParens": "always"
}
```

### .prettierignore

```
dist
node_modules
.git
package.json
package-lock.json
```

## Common Tasks

### Add New Vue Component with Dependencies

```bash
# Install Element Plus table component
npm install @element-plus/table

# Or install icon
npm install @element-plus/icons-vue
```

### Update Dependencies

```bash
# Check for updates
npm outdated

# Update minor/patch versions
npm update

# Update specific package
npm install --save axios@latest

# Update to latest major version
npm install --save-dev vite@latest
```

### Fix Dependency Issues

```bash
# Clean install
rm -rf node_modules package-lock.json
npm install

# Audit for vulnerabilities
npm audit

# Fix vulnerabilities
npm audit fix
```

### Production Build

```bash
# Build optimized for production
npm run build

# Check output size
npm install -g size-limit
size-limit dist/

# Analyze bundle
npm install -g source-map-explorer
source-map-explorer 'dist/*.js'
```

## Version Management

### Semantic Versioning Symbols

- `^` - Compatible with version (allows minor and patch updates)
- `~` - Reasonably close to version (allows patch updates only)
- `*` - Latest version
- `1.2.3` - Exact version
- `>=1.2.3` - Version and above

### Updating package.json

```json
{
  "dependencies": {
    "vue": "^3.3.13",      // Can update to 3.x.x
    "axios": "~1.6.5"      // Can update to 1.6.x only
  }
}
```

## Docker Build

### Dockerfile for Frontend

```dockerfile
# Build stage
FROM node:18-alpine as builder

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

## Performance Tips

1. **Lazy Load Routes**: Code split page components with `defineAsyncComponent`
2. **Tree Shake**: Remove unused imports
3. **Compress Assets**: Images and videos should be optimized
4. **Minify CSS/JS**: Vite does this automatically in production
5. **Optimize Dependencies**: Use dynamic imports for large libraries

## Common Issues

### Issue: npm install fails

```bash
# Try clean install
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Issue: Module not found

```bash
# Reinstall dependencies
npm install

# Clear Vite cache
rm -rf node_modules/.vite
npm install
```

### Issue: Port 5173 already in use

```bash
# Change port in vite.config.js or use CLI
npm run dev -- --port 5174
```
