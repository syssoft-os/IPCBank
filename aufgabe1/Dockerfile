FROM openjdk:11

# Set default values for environment variables
ENV NUM_ACCOUNTS 1000
ENV NUM_CLIENTS 100
ENV TRANSACTIONS_PER_CLIENT 1000000

COPY src /app
WORKDIR /app
RUN javac BankSimulation.java

CMD ["java", "BankSimulation"]
