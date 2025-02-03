from pathlib import Path
import logging

from .parsing.lexer import WDLLexer
from .parsing.parser import WDLParser
from .garmin.client import GarminClient
from .garmin.visitor import GarminVisitor

def process_wdl_file(file_path: Path, parser):
    """Process a single wdl file and return the AST"""
    logging.info(f"Processing wdl file: {file_path}")
    try:
        with open(file_path, 'r') as f:
            data = f.read()
        
        result = parser.parse(data)
        return result
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {str(e)}")
        logging.exception(e)
        return None

__all__ = ['WDLLexer', 'WDLParser', 'GarminClient', 'GarminVisitor', 'process_wdl_file']