#!/bin/bash

# Run the Java process in the foreground
java BankServer &

# Check if the NUM_CLIENTS environment variable is set in docker, default to 1 if not set
NUM_CLIENTS=${NUM_CLIENTS:-100}

# Run other Java processes in the background

for ((i=1; i<=$NUM_CLIENTS; i++)); do
  java BankClient &
done

# Wait for the foreground process to finish (or use another mechanism)
wait
