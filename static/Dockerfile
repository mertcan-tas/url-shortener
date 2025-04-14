FROM node:18-alpine AS build-stage

# Gerekli paketleri yükle
RUN apk add --no-cache python3 make g++ git

WORKDIR /app

# Önce package.json kopyala ve yükle
COPY package*.json ./
RUN npm install

# Sonra geri kalan dosyaları kopyala
COPY . .

# Build komutunu çalıştır
RUN NODE_ENV=production npm run build

FROM nginx:stable-alpine AS production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]