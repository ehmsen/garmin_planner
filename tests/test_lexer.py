import pytest
from garmin_planner import WorkoutLexer

def test_lexer_tokenizes_workout_step(lexer):
    input_text = "run 5.0 @ epace"
    lexer.input(input_text)
    
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    
    assert len(tokens) == 4
    assert tokens[0].type == 'RUN'
    assert tokens[1].type == 'FLOAT'
    assert tokens[2].type == 'AT'
    assert tokens[3].type == 'ID'