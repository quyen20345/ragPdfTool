FROM node:20-alpine

WORKDIR /app
COPY package*.json /app
RUN npm i --silent
RUN npm i -g react-scripts@5.0.1

CMD [ "npm", "start" ]