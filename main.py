import argparse
import logging
from pathlib import Path
from wdl import WDLLexer, WDLParser, GarminClient, GarminVisitor, process_wdl_file
import json

from wdl.utils import logger

def main():
    parser = argparse.ArgumentParser(
        description="Process Workout DSL files and upload to Garmin Connect"
    )
    parser.add_argument(
        'files',
        type=Path,
        nargs='+',
        help='One or more workout DSL files to process'
    )
    parser.add_argument(
        '--log-file',
        type=str,
        help='Path to log file (if not specified, logs to stdout only)'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Set the logging level'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logger.setup_logging(args.log_file, args.log_level)
    
    # Initialize parser and lexer
    lexer = WDLLexer()
    lexer.build()
    parser = WDLParser(lexer)
    parser.build()
    
    # Process each file
    for file_path in args.files:
        if not file_path.exists():
            logging.error(f"File not found: {file_path}")
            continue
            
        workout_ast = process_wdl_file(file_path, parser)
        # import pprint
        # pprint.pp(workout_ast)
        if workout_ast:
            try:
                visitor = GarminVisitor()
                garmin_workouts = visitor.visit(workout_ast)
                # import pprint
                # garmin_json_dict['workoutId'] = 42
                # pprint.pp(garmin_json_dict)
                if visitor.username and visitor.password:
                    # client = GarminClient(visitor.username, visitor.password)
                    # out = client.getWorkout(42)
                    # out = client.getAllWorkouts()
                    # import pprint
                    # pprint.pp(out)

                    for garmin_workout in garmin_workouts:
                        garmin_workout_json = json.dumps(garmin_workout)
                        # import pprint
                        # pprint.pp(garmin_workout_json)
                        # client.importWorkout(garmin_workout_json)
                    logging.info(f"Successfully uploaded workout from {file_path}")
            except Exception as e:
                logging.exception(f"Error uploading workout from {file_path}: {str(e)}")
                raise e

if __name__ == '__main__':
    main()