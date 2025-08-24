# --- Stage 1: The "Workshop" to build the React app ---
FROM node:20-alpine AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install all dependencies
RUN npm install

# Copy the rest of the source code
COPY . .

# Run the build command to create optimized static files
RUN npm run build


# --- Stage 2: The "Showroom" to serve the final app ---
FROM nginx:stable-alpine

# Copy the optimized files from the "Workshop" stage
COPY --from=build /app/dist /usr/share/nginx/html

# Tell Docker the container will listen on port 80
EXPOSE 80

# The command to start the Nginx web server
CMD ["nginx", "-g", "daemon off;"]