#!/usr/bin/env bash
set -euo pipefail

BROKER="${KAFKA_BOOTSTRAP_SERVERS:-localhost:9092}"

kafka-topics --bootstrap-server "$BROKER" --create --if-not-exists --topic orders --partitions 3 --replication-factor 1
kafka-topics --bootstrap-server "$BROKER" --create --if-not-exists --topic orders.dlq --partitions 3 --replication-factor 1

echo "Kafka topics ready: orders, orders.dlq"
