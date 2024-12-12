FROM docker.io/node:23 
WORKDIR /app
COPY package*.json ./
RUN npm install
RUN npm upgrade
COPY . .
EXPOSE 3000
ENTRYPOINT ["npm", "start"]
