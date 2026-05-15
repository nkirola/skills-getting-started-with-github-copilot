import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_activities():
    """Save a deep copy of the in-memory `activities` before each test
    and restore it after the test so tests are isolated.
    """
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)
