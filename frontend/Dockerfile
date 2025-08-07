FROM node:18-alpine
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies + typography plugin
RUN npm install \
 && npm install -D @tailwindcss/typography

# Copy source code
COPY . .

EXPOSE 3000
CMD ["npm", "start"]
