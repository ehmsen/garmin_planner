import pytest
from garmin_planner import WorkoutParser

def test_parser_parses_simple_workout(parser, lexer):
    input_text = '''
    run "Simple Workout" {
        run 5.0 @ 5:00 - 5:30
    }
    '''
    result = parser.parse(input_text, lexer=lexer)
    assert result is not None
    assert len(result.children) == 1