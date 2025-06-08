
set dotenv-load

app_file := "src/app/__main__.py"

export APP_PATH := "src/app"

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
test target="src/app/tests" *ARGS:
  SERVER_DEBUG=true \
  SERVER_TESTING=true  \
  LOGGING_APP_LEVEL=DEBUG \
  uv run pytest --disable-warnings {{ target }} {{ ARGS }}
