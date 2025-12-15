FROM node:18-alpine as builder

WORKDIR /app

COPY package*.json ./

# npm ci often fails in Docker with "Exit handler never called" but dependencies are actually installed
# So we ignore the error and verify vite exists before continuing
RUN npm ci || true && \
    if [ ! -f node_modules/.bin/vite ]; then \
        echo "Retrying with npm install..."; \
        rm -rf node_modules package-lock.json; \
        npm install; \
    fi

COPY . .

ARG VITE_API_BASE_URL=/api
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build


FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
