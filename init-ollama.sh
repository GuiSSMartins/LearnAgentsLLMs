#!/bin/sh

echo "Starting Ollama..."

ollama serve &

SERVER_PID=$!

echo "Waiting for Ollama..."

until ollama list >/dev/null 2>&1
do
    sleep 1
done

echo "Downloading model if necessary..."

ollama pull "$OLLAMA_MODEL"

echo "Ready."

wait $SERVER_PID