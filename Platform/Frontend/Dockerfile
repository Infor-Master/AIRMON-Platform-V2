FROM node:14.15.4

# make the 'app' folder the current working directory
RUN mkdir /app
WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies
# outras dependências TEEM de ser adicionadas no package.json
COPY package.json /app/package.json

RUN npm install

# start app
#CMD ["npm", "run", "serve"]
CMD http-server dist -p 89