# Multi-stage build for Next.js app with Python support
FROM node:18-bullseye

# Install Python 3
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install Node dependencies
RUN npm install

# Copy application files
COPY . .

# Expose port 3000
EXPOSE 3000

# Set environment variable
ENV NODE_ENV=development

# Start Next.js development server
CMD ["npm", "run", "dev"]
