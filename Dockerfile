FROM node:18

WORKDIR /usr/src/app

COPY src/package*.json ./

RUN npm install

COPY src .

EXPOSE 8999

CMD [ "node", "app.js" ]

