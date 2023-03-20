FROM node:14

COPY . .

WORKDIR /app
RUN npm install -g @vue/cli

RUN npm install

EXPOSE 3000

CMD ["npm", "run", "dev"]