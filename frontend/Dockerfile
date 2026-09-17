FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

# Use for ECS health check.
RUN apk add --no-cache curl   

COPY . .

EXPOSE 8000

CMD ["node", "server.js"]