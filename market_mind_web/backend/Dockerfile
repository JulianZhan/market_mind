# Use the official Java Runtime Environment (JRE) base image
FROM openjdk:21-slim

# The application's jar file
ARG JAR_FILE=target/*.jar

# Add the application's jar to the container
COPY ${JAR_FILE} app.jar

# Specify the default command to run on boot
ENTRYPOINT ["java","-jar","/app.jar"]
