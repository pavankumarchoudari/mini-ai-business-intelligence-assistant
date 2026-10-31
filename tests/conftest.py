import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from backend.database import initialize_database

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    initialize_database(force_reload=True)
