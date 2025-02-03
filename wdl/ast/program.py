from .base import ASTNode
import logging

logger = logging.getLogger(__name__)

class ProgramNode(ASTNode):
    def __init__(self, name, weeks):
        super().__init__(children=weeks)
        self.name = name
        self.weeks = {w.week_num: w for w in weeks}

    def get_duration_estimate(self):
        return sum([week.get_duration_estimate() for week in self.weeks.values()])
    
    def get_distance_estimate(self):
        return sum([week.get_distance_estimate() for week in self.weeks.values()])

class ProgramWeekNode(ASTNode):
    def __init__(self, week_num, workouts):
        super().__init__(children=workouts)
        self.week_num = week_num
        self.workouts = workouts

    def get_duration_estimate(self):
        return sum([workout.get_duration_estimate() for workout in self.workouts])
    
    def get_distance_estimate(self):
        return sum([workout.get_distance_estimate() for workout in self.workouts])