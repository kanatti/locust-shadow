# Echo Server

This is a simple echo server implemented using FastAPI. It provides a GET endpoint that echoes back JSON data.

## Usage

To start the server, run:

```bash
uv run --package echo-server ./packages/echo-server/main.py
```

The server will start on `http://localhost:8000`.

## API Endpoints

### GET /echo

Echoes back the JSON data sent in the request.

Example:
```bash
curl -X GET "http://localhost:8000/echo?data={\"message\":\"Hello, World!\"}"
```

Response:
```json
{"message": "Hello, World!"}
```

## Development

This echo server is part of the larger Locust-Shadow project. It serves as a simple target for testing and demonstrating the capabilities of Locust-Shadow.

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](../../LICENSE) file for details.
