import pytest
from fastapi.testclient import TestClient
from echo_server.main import app

client = TestClient(app)

def test_echo_valid_json_no_delay():
    response = client.get("/echo", params={"data": '{"key": "value"}'})
    assert response.status_code == 200
    assert response.json() == {"data": {"key": "value"}}

def test_echo_invalid_json():
    response = client.get("/echo", params={"data": 'invalid json'})
    assert response.status_code == 200
    assert response.json() == {"data": {"error": "Invalid JSON"}}

def test_echo_with_delay():
    response = client.get("/echo", params={"data": '{"key": "value"}', "delay_ms": 10})
    assert response.status_code == 200
    assert response.json() == {"data": {"key": "value"}}

def test_echo_min_delay():
    response = client.get("/echo", params={"data": '{"key": "value"}', "delay_ms": 0})
    assert response.status_code == 200
    assert response.json() == {"data": {"key": "value"}}

@pytest.mark.parametrize("input_data,expected", [
    ('{"message": "Hello"}', {"data": {"message": "Hello"}}),
    ('{"message": "World"}', {"data": {"message": "World"}}),
])
def test_echo_parametrized(input_data, expected):
    response = client.get("/echo", params={"data": input_data})
    assert response.status_code == 200
    assert response.json() == expected
