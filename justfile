
set dotenv-load

app_file := "app/__main__.py"

export APP_PATH := "app"

# ex: just server --port 8000 --host 0.0.0.0 
dev *ARGS:
  DB_DEV=true \
  SERVER_DEBUG=true \
  LOGGING_APP_LEVEL=DEBUG \
  uv run fastapi dev --reload {{ app_file }} {{ ARGS }}

# ex: just fastapi prepare_db
fastapi *ARGS:
  uv run fastapi {{ ARGS }}

# ex: just test tests/integration -v -s --show-capture=all [--log-cli-level=INFO | -p no:logging]
test target="tests" *ARGS:
  SERVER_DEBUG=true \
  SERVER_TESTING=true  \
  LOGGING_APP_LEVEL=DEBUG \
  uv run pytest --disable-warnings {{ target }} {{ ARGS }}


podman-rund-kafka:
  podman network create --name devlab.dev

  podman pod create --name kafka-pod --network devlab.dev

  podman run --rm --name zookeeper --network devlab.dev \
    -e ZOOKEEPER_CLIENT_PORT=2181 \
    -e ZOOKEEPER_TICK_TIME=2000 \
    -e ZOOKEEPER_INIT_LIMIT=5 \
    -e ZOOKEEPER_SYNC_LIMIT=2 \
    --pod kafka-pod \
    quay.io/wurstmeister/zookeeper

  podman run --rm --name kafka-ui --network devlab.dev \
    -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
    --pod kafka-pod \
    quay.io/wurstmeister/kafka-ui

  podman run --rm --name kafka --network devlab.dev \
    -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
    -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092 \
    --pod kafka-pod \
    quay.io/wurstmeister/kafka
