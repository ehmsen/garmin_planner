import logging
import sys
from pathlib import Path

def setup_logging(log_file=None, log_level='INFO'):
    """Configure logging based on command line arguments."""
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatters
    console_format = '%(levelname)s: %(message)s'
    file_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(numeric_level)
    
    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter(console_format))
    logger.addHandler(console)
    
    # File handler if specified
    if log_file:
        log_path = Path(log_file)
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(logging.Formatter(file_format))
        logger.addHandler(file_handler)