FROM docker.io/node:23 
LABEL mainatainer="CPA <cpa@uem.br>"
LABEL br.uem.cpa.sistema.frontend.author="Arthur Ueda"
LABEL br.uem.cpa.sistema.frontend.version="v010"
WORKDIR /app
COPY package*.json ./
RUN npm install
RUN npm upgrade
COPY . .
EXPOSE 3000
ENTRYPOINT ["npm", "start"]
