FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install --production

# Copy Prisma schemas
COPY cloud-schema.prisma ./
COPY payments-schema.prisma ./

# Generate Prisma clients
RUN npx prisma generate --schema=cloud-schema.prisma
RUN npx prisma generate --schema=payments-schema.prisma

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => { process.exit(r.statusCode === 200 ? 0 : 1); })"

# Start the webhook server
CMD ["npm", "start"]
