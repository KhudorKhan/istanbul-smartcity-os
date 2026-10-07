# ---- Stage 1: build the Spring Boot fat jar ----
FROM maven:3.9.6-eclipse-temurin-17 AS builder
WORKDIR /app

COPY pom.xml .
RUN mvn -B -q dependency:go-offline

COPY src ./src
RUN mvn -B clean package -DskipTests \
    && cp target/smartcity-financial-backend-*.jar target/app.jar

# ---- Stage 2: minimal JRE runtime ----
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

COPY --from=builder /app/target/app.jar app.jar

EXPOSE 8080

HEALTHCHECK --interval=15s --timeout=5s --start-period=45s --retries=5 \
    CMD wget -q --spider http://localhost:8080/actuator/health || exit 1

ENTRYPOINT ["java", "-jar", "app.jar"]
