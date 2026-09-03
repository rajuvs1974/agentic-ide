from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_agent_task() -> None:
    response = client.post(
        "/api/v1/agent/tasks",
        json={
            "instruction": "Create a FastAPI health endpoint",
            "workspace": "/workspace/demo",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["instruction"] == "Create a FastAPI health endpoint"
    assert data["workspace"] == "/workspace/demo"
    assert data["status"] == "completed"
    assert data["task_id"]
