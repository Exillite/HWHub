# Use an official Node.js runtime as the base image
FROM node:16

COPY . .
WORKDIR /app

RUN npm install

EXPOSE 8080

CMD ["npm", "run", "serve"]