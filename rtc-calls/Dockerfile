FROM node:14

COPY . .

WORKDIR /app


RUN rm -rf package-lock.json
RUN rm -rf node_modules
RUN rm -rf .parcel-cache
RUN rm -rf dist

RUN npm cache clean --force

RUN npm install

RUN npm run test

EXPOSE 9966

CMD ["npm", "run", "start"]