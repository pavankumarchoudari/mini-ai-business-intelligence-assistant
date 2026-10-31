from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_ask_endpoint_returns_structured_answer():
    response = client.post('/ask', json={'question': 'What is the total revenue?'})
    assert response.status_code == 200
    body = response.json()
    assert body['intent'] == 'total_revenue'
    assert body['data']['total_revenue'] > 0
    assert body['answer']

def test_unsupported_question_returns_422():
    response = client.post('/ask', json={'question': 'Tell me a joke'})
    assert response.status_code == 422

def test_too_short_question_is_rejected():
    response = client.post('/ask', json={'question': 'hi'})
    assert response.status_code == 422
