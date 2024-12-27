# locust-shadow

`locust-shadow` is a library that extends Locust to provide warmup and shadow testing capabilities.

## Usage

`locust-shadow` is designed to be used as a library in your Locust test scripts. It provides two main functionalities:

1. Warmup testing
2. Shadow testing

For examples of how to use `locust-shadow`, please refer to the `examples` package in this repository.

### Warmup Testing

To run a warmup test, you can use the `WarmupConfig` and `run_warmup` function from `locust_shadow`. Here's a basic example:

```python
from locust_shadow.config import WarmupConfig
from locust_shadow.runner import run_warmup

warmup_config = WarmupConfig.from_yaml('path/to/your/warmup_config.yaml')
run_warmup(warmup_config)
```

### Shadow Testing

To run a shadow test, you can use the `ShadowConfig` and `run_shadow` function from `locust_shadow`. Here's a basic example:

```python
from locust_shadow.config import ShadowConfig
from locust_shadow.runner import run_shadow

shadow_config = ShadowConfig.from_yaml('path/to/your/shadow_config.yaml')
run_shadow(shadow_config)
```

## Configuration

Both warmup and shadow tests are configured using YAML files. For details on the configuration options, please refer to the documentation or the example configuration files in the `examples` package.

## Examples

For full examples of how to use `locust-shadow`, including command-line scripts for running tests, please see the `examples` package in this repository.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
