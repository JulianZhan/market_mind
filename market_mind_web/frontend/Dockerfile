# Use an official node runtime as the base image
FROM node:16

# Set the working directory in the container to /app
WORKDIR /app

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . .

# Install the dependencies in the container
RUN npm install

# Build the React app
RUN npm run build

# Expose port 3000 for the app to be accessible outside
EXPOSE 3000

# Use serve to serve the production build of your React app
RUN npm install -g serve

# Command to run the application
CMD ["serve", "-s", "build", "-l", "3000"]
