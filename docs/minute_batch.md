# Minute Batch Specification

## Overview
Minute batches are the core of Locust-Shadow, representing traffic patterns extracted from production logs. Each batch contains request data for a specific minute of traffic, along with metadata about the traffic volume and characteristics.

## Directory Structure
```
minute_batches/
├── minute_0/
├── minute_1/
├── minute_2/
└── ...
```

## Minute Batch Contents
Each minute directory contains:
1. A metadata file
2. One or more request files

### Metadata File
- **Filename**: `metadata.json`
- **Format**: JSON
- **Content**:
  ```json
  {
    "tps": 100,
    "total_requests": 6000,
    "timestamp": "2023-05-01T12:00:00Z"
  }
  ```
  - `tps`: Target transactions per second for this minute
  - `total_requests`: Total number of requests in this minute batch
  - `timestamp`: Start time of this minute batch

### Request Files
- **Filename**: `requests.jsonl` (or `requests_0.jsonl`, `requests_1.jsonl` if split into multiple files)
- **Format**: JSON Lines (JSONL)
- **Content**: Each line represents a single request in JSON format
  ```jsonl
  {"method": "GET", "path": "/api/users", "headers": {"Content-Type": "application/json"}, "query_params": {"page": 1}, "body": null}
  {"method": "POST", "path": "/api/orders", "headers": {"Content-Type": "application/json"}, "body": {"product_id": 123, "quantity": 2}}
  ```

## Example Minute Batch
```
minute_batches/
└── minute_0/
    ├── metadata.json
    └── requests.jsonl
```

### metadata.json
```json
{
  "tps": 100,
  "total_requests": 6000,
  "timestamp": "2023-05-01T12:00:00Z"
}
```

### requests.jsonl
```jsonl
{"method": "GET", "path": "/api/users", "headers": {"Content-Type": "application/json"}, "query_params": {"page": 1}, "body": null}
{"method": "POST", "path": "/api/orders", "headers": {"Content-Type": "application/json"}, "body": {"product_id": 123, "quantity": 2}}
{"method": "GET", "path": "/api/products", "headers": {"Content-Type": "application/json"}, "query_params": {"category": "electronics"}, "body": null}
```

## Usage
The Locust executor will read the metadata to determine the target TPS and then process the requests from the JSONL file(s) to generate the appropriate load pattern.
