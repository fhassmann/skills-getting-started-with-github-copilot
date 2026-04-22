from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def restore_activities_state():
    """Reset global in-memory state between tests to avoid cross-test pollution."""
    original = deepcopy(activities)
    yield
    activities.clear()
    activities.update(deepcopy(original))
