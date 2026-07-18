# --- Stage 1: Compile and Build React Assets ---
FROM node:20-alpine AS builder
WORKDIR /app

# Install package dependencies first for rapid builds
COPY package*.json ./
RUN npm install

# Copy the rest of the application files and compile production builds
COPY . .
RUN npm run build

# --- Stage 2: Serve compiled web bundles using Nginx ---
FROM nginx:stable-alpine

# Copy compiled build output files over to the default Nginx web root directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose standard production HTTP proxy port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
