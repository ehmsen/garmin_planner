from pathlib import Path
import logging

from .lexer import WorkoutLexer
from .parser import WorkoutParser
from .client import GarminClient
from .garmin import GarminVisitor

def process_wdl_file(file_path: Path, parser, lexer):
    """Process a single wdl file and return the AST"""
    logging.info(f"Processing wdl file: {file_path}")
    try:
        with open(file_path, 'r') as f:
            data = f.read()
        
        result = parser.parse(data, lexer)
        return result
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {str(e)}")
        return None


__all__ = ['WorkoutLexer', 'WorkoutParser', 'GarminClient', 'GarminVisitor', 'process_wdl_file']