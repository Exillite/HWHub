# Use an official Node.js runtime as the base image
FROM node:14

COPY . .
WORKDIR /app
RUN npm install -g @vue/cli

RUN npm install

EXPOSE 8080

CMD ["npm", "run", "serve"]