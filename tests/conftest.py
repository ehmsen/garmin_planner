import pytest
from pathlib import Path
from garmin_planner import WorkoutLexer, WorkoutParser, GarminVisitor

@pytest.fixture
def test_data_dir():
    return Path(__file__).parent / "test_data"

@pytest.fixture
def lexer():
    return WorkoutLexer().build()

@pytest.fixture
def parser():
    return WorkoutParser().build()

@pytest.fixture
def visitor():
    return GarminVisitor()