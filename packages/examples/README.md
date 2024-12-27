# Locust Shadow Examples

This package contains examples demonstrating how to use the `locust_shadow` library for warmup and shadow testing.

## Available Examples

1. **Warmup Test**: Demonstrates how to run a warmup test using `locust_shadow`.
2. **Shadow Test**: Shows how to perform shadow testing with `locust_shadow`.

## Running the Examples

You can run these examples from the workspace root using the `uv` command. Here are the commands for each example:

### Warmup Test

```
uv run --package examples warmup -c ./dev/warmup-config.yaml
```

### Shadow Test

```
uv run --package examples shadow -c ./dev/shadow-config.yaml
```

## Configuration Files

Both examples use YAML configuration files:

- `./dev/warmup-config.yaml`: Configuration for the warmup test
- `./dev/shadow-config.yaml`: Configuration for the shadow test

Ensure these configuration files exist and are properly set up before running the examples.

## Using Echo-Server with Dev Configurations

When using the dev configurations (`./dev/warmup-config.yaml` and `./dev/shadow-config.yaml`), you'll need to run the echo-server to handle the requests. The echo-server is a simple HTTP server that echoes back the requests it receives, which is useful for testing purposes.

To run the echo-server:

1. Open a new terminal window.
2. Navigate to the workspace root.
3. Run the following command:

```
uv run --package echo-server echo_server
```

This will start the echo-server on `http://localhost:8000` by default. Ensure the echo-server is running before starting your warmup or shadow tests using the dev configurations.

The dev configurations are set up to send requests to `http://localhost:8000`, which matches the default echo-server address. If you modify the echo-server address or port, make sure to update the configurations accordingly.
