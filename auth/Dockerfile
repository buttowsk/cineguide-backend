FROM maven:3.8.4-openjdk-17-slim AS build-spring

WORKDIR /app

COPY ./pom.xml .

RUN mvn -f pom.xml dependency:go-offline

COPY ./src ./src

RUN mvn -f pom.xml package


FROM openjdk:17-jdk-slim

WORKDIR /auth

COPY --from=build-spring /app/target/*.jar /auth/app.jar

EXPOSE 8081

ENTRYPOINT ["java", "-jar", "app.jar"]