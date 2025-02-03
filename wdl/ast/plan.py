from .base import ASTNode

class PlanNode(ASTNode):
    def __init__(self, name, date, week):
        super().__init__(children=week)
        self.name = name
        self.date = date
        self.week = week

class PlanWeekNode(ASTNode):
    def __init__(self, workout_days):
        super().__init__(children=workout_days)
        
        week_day_dict = {"mon": "monday", "tue": "tuesday", "wed": "wednesday", "thu": "thursday", "fri": "friday", "sat": "saturday", "sun": "sunday"}
        workout_days = [(
            d[0].lower() if d[0].lower() in week_day_dict.values() else week_day_dict[d[0].lower()],
            d[1]) for d in workout_days]

        days = [d[0] for d in workout_days]
        if len(days) != len(set(days)):
            raise ValueError("Duplicate day in plan week")

        self.workout_days = dict(workout_days)