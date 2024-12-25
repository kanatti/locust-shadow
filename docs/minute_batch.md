# Minute Batch Specification

## Overview
Minute batches are the core of Locust-Shadow, representing traffic patterns extracted from production logs. Each batch contains request data for a specific minute of traffic, along with configuration about the traffic volume.

## Configuration
The minute batch configuration is now part of the main configuration file (e.g., `test-config.yaml`). This allows for a more centralized and flexible setup.

### Configuration File Structure
```yaml
host: "http://localhost:8000"
minute_batches:
  - rps: 2
    request_files:
      - "./dev/test_minute_batch_01/requests1.jsonl"
  - rps: 4
    request_files:
      - "./dev/test_minute_batch_01/requests2.jsonl"
```

- `host`: The target host for the shadow traffic
- `minute_batches`: A list of minute batch configurations
  - `rps`: Requests per second for this minute batch
  - `request_files`: List of JSONL files containing the requests for this minute batch

## Request Files
- **Format**: JSON Lines (JSONL)
- **Content**: Each line represents a single request in JSON format
  ```jsonl
  {"timestamp": "2023-05-01T00:00:01", "method": "GET", "path": "/echo", "params": {"data": "{\"message\":\"Hello, World!\"}"}}
  ```

## Example Request File (requests1.jsonl)
```jsonl
{"timestamp": "2023-05-01T00:00:01", "method": "GET", "path": "/echo", "params": {"data": "{\"message\":\"Hello, World!\"}"}}
{"timestamp": "2023-05-01T00:00:03", "method": "GET", "path": "/echo", "params": {"data": "{\"name\":\"John Doe\",\"age\":30}"}}
{"timestamp": "2023-05-01T00:00:05", "method": "GET", "path": "/echo", "params": {"data": "{\"colors\":[\"red\",\"green\",\"blue\"]}"}}
{"timestamp": "2023-05-01T00:00:08", "method": "GET", "path": "/echo", "params": {"data": "{\"status\":\"active\",\"count\":42}"}}
{"timestamp": "2023-05-01T00:00:10", "method": "GET", "path": "/echo", "params": {"data": "{\"error\":null,\"success\":true}"}}
```

## Usage
The Locust executor will read the configuration to determine the target RPS for each minute batch and then process the requests from the specified JSONL file(s) to generate the appropriate load pattern. Each minute batch will run for 60 seconds before moving to the next one.

The total duration of the shadow run will be the number of minute batches multiplied by 60 seconds. For example, if there are 2 minute batches in the configuration, the total run time will be 120 seconds (2 minutes).
