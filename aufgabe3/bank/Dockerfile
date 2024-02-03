FROM clojure:latest

WORKDIR /usr/src/app

# Set default values for environment variables
ENV NUM_ACCOUNTS 1000
ENV NUM_CLIENTS 100
ENV NUM_TRANSFERS 1000000

COPY . .

RUN lein uberjar
RUN ls

CMD ["java", "-jar", "target/uberjar/bank_simulation.jar"]