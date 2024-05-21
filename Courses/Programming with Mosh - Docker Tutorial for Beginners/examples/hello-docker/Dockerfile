# specify runtime env (node) and OS (alpine lightweight linux)
FROM node:alpine

# specify the files to be copied (.) and the destination address (/app)
COPY . /app

# change the cwd of the image
WORKDIR /app

# command to run the application
CMD node app.js

