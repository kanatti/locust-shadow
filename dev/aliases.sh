locust_shadow() {
  uv run --package locust-shadow cli "$@"
}

run_shadow() {
  locust_shadow shadow ./dev/shadow-config.yaml "$@"
}

run_warmup() {
  locust_shadow warmup ./dev/warmup-config.yaml "$@"
}

alias run-echo-server="uv run --package echo-server cli"
