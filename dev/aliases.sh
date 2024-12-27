locust_shadow() {
  uv run --package locust-shadow locust_shadow "$@"
}

run_shadow() {
  locust_shadow shadow ./dev/shadow-config.yaml "$@"
}

run_warmup() {
  locust_shadow warmup ./dev/warmup-config.yaml "$@"
}

alias run_echo_server="uv run --package echo-server echo_server"
