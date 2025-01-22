import logging
import garth
from garth.exc import GarthException

SESSION_DIR = '.garth'

logger = logging.getLogger(__name__)

class GarminClient(object):
    def __init__(self, email, password):
        logger.info(f"Initializing Garmin client for user: {email}")
        self._email = email
        self._password = password

        if not self.login():
            raise Exception("Login failed")
     
    def getAllWorkouts(self) -> dict:
        logger.info("Fetching all workouts")
        return garth.connectapi(f"""/workout-service/workouts""",
                                params={"start": 1, "limit": 999, "myWorkoutsOnly": True, "sharedWorkoutsOnly": False, "orderBy": "WORKOUT_NAME", "orderSeq": "ASC", "includeAtp": False})

    def getWorkout(self, workoutId: str) -> dict:
        logger.info(f"Fetching workout with ID: {workoutId}")
        return garth.connectapi(f"""/workout-service/workout/{workoutId}""")

    def deleteWorkout(self, workout: dict) -> bool:
        logger.info(f"Deleting workout with ID: {workout['workoutId']}")
        res = garth.connectapi(f"""/workout-service/workout/{workout['workoutId']}""",
                               method="DELETE")
        if res != None:
            logging.info(f"""Deleted workoutId: {workout['workoutId']} workoutName: {workout['workoutName']}""")
            return True
        else:
            logging.warn(f"""Could not delete workout. Workout not found with workoutId: {workout['workoutId']} (workoutName: {workout['workoutName']})""")
            return False

    def scheduleWorkout(self, id, dateJson: dict) -> bool:
        logger.info(f"Scheduling workout with ID: {id}")
        resJson = garth.connectapi(f"""/workout-service/schedule/{id}""",
                               method="POST",
                               headers={'Content-Type': 'application/json'},
                               json=dateJson)
        if ('workoutScheduleId' not in resJson):
            return False
        return True

    def importWorkout(self, workoutJson) -> dict:
        logger.info("Uploading workout to Garmin Connect")
        logger.debug(f"Workout data: {workoutJson}")
        resJson = garth.connectapi(f"""/workout-service/workout""",
                               method="POST",
                               headers={'Content-Type': 'application/json'},
                               data=workoutJson)
        logging.info(f"""Imported workout {resJson['workoutName']}""")
        return resJson
    
    def login(self) -> bool:
        logger.info("Logging in to Garmin Connect")
        try:
            garth.resume(SESSION_DIR)
            garth.client.username
        except (FileNotFoundError, GarthException):
            garth.login(self._email, self._password)
            garth.save(SESSION_DIR)
        return True