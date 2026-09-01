from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    # فحص مرن يتأكد من وجود رسالة ترحيبية أو الحالة العامة للخدمة
    response_json = response.json()
    message_content = response_json.get("message", "") or response_json.get("service", "")
    assert len(message_content) > 0

def test_create_and_duplicate_ticket():
    ticket_data = {
        "id": "t-test-999",
        "subject": "Test billing issue",
        "body": "Charged wrongly"
    }
    
    # First creation -> 202 Accepted
    response = client.post("/tickets/", json=ticket_data)
    assert response.status_code == 202
    data = response.json()
    assert data["id"] == "t-test-999"
    # فحص واقعي يقبل الحالة المعلقة أو التي تم تصنيفها بسرعة فائقة بواسطة الـ Worker
    assert data["status"] in ["pending", "classified"]
    
    # Duplicate creation -> should return existing ticket without re-creating/error
    response_dup = client.post("/tickets/", json=ticket_data)
    assert response_dup.status_code == 202
    assert response_dup.json()["id"] == "t-test-999"

def test_get_nonexistent_ticket():
    response = client.get("/tickets/non-existent-id")
    assert response.status_code == 404