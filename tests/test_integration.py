import pytest
from pathlib import Path
from wdl import process_wdl_file

def test_end_to_end_workflow(test_data_dir, lexer, parser):
    workout_file = test_data_dir / "valid_wdls/simple.wdl"
    result = process_wdl_file(workout_file, parser, lexer)
    assert result is not None