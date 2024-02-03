FROM openjdk:11

# Set default values for environment variables
ENV NUM_ACCOUNTS 1000
ENV TRANSACTIONS_PER_CLIENT 1000000
ENV NUM_CLIENTS 100

COPY src /app
COPY run_server_and_clients.sh /app
WORKDIR /app
RUN javac *.java

RUN chmod +x run_server_and_clients.sh
ENTRYPOINT ["./run_server_and_clients.sh"]