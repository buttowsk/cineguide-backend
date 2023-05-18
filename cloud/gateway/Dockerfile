FROM maven:3.8.4-openjdk-17-slim AS build-apigateway

WORKDIR /app

COPY ./pom.xml .

RUN mvn -f pom.xml dependency:go-offline

COPY ./src ./src

RUN mvn -f pom.xml package

FROM openjdk:17-jdk-slim

WORKDIR /app

COPY --from=build-apigateway /app/target/*.jar /app/app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]