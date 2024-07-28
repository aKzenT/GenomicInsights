# Start from the official Node.js base image
FROM node:16

# Set the working directory in the Docker container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on, if necessary
# EXPOSE <port_number>

# Define the command to run the app
CMD ["npm", "start"]