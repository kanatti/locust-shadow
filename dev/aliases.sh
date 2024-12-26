locust_shadow() {
  uv run --package locust-shadow ./packages/locust-shadow/main.py "$@"
}

run_shadow() {
  locust_shadow shadow ./dev/shadow-config.yaml "$@"
}

run_warmup() {
  locust_shadow warmup ./dev/warmup-config.yaml "$@"
}

alias run-echo-server="uv run --package echo-server ./packages/echo-server/main.py"