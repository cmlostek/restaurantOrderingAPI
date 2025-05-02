from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture(scope='module')
def seeded_client():
    return client


def test_create_new_resource(seeded_client):
    resource_create_request = {
        "resource_id": 999,
        "resource_name": "Test Resource",
        "resource_type": "Type A",
        "quantity_available": 10
    }

    response = seeded_client.post("/resources/", json=resource_create_request)
    assert response.status_code == 200
    assert response.json() == {
        "resource_id": 999,
        "resource_name": "Test Resource",
        "resource_type": "Type A",
        "quantity_available": 10
    }


def test_get_all_resources(seeded_client):
    response = seeded_client.get('/resources/')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(resource['resource_id'] == 1 for resource in data)

def test_get_resource_by_id(seeded_client):
    response = seeded_client.get("/resources/1")
    assert response.status_code == 200
    data = response.json()

    assert data == {
        "resource_id": 1,
        "resource_name": "Tomatoes",
        "resource_type": "Produce",
        "quantity_available": 50
    }

def test_update_existing_resource(seeded_client):
    resource_update_request = {
        "resource_id": 1,
        "resource_name": "Updated Tomatoes",
        "resource_type": "Produce",
        "quantity_available": 60
    }

    response = seeded_client.put("/resources/1", json=resource_update_request)
    assert response.status_code == 200
    assert response.json() == {
        "resource_id": 1,
        "resource_name": "Updated Tomatoes",
        "resource_type": "Produce",
        "quantity_available": 60
    }

def test_delete_existing_resource(seeded_client):
    response = seeded_client.delete("/resources/3")
    assert response.status_code == 200
    assert response.json() == {
            "resource_id": 3,
            "resource_name": "Ground Beef",
            "resource_type": "Meat",
            "quantity_available": 15
        }


    response = seeded_client.get("/resources/3")
    assert response.status_code == 404
    assert response.json() == {"detail": "Resource not found"}



