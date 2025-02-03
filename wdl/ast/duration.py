from .base import ASTNode

durations_defintions = {}

class DurationASTNode(ASTNode):
    def __init__(self, children=None, leaf=None):
        super().__init__(children, leaf)

    def get_duration(self):
        return None
    
    def get_distance(self):
        return None

class DurationsNode(ASTNode):
    def __init__(self, definitions):
        super().__init__(children=definitions)
        self.definitions = definitions

class DurationDefNode(ASTNode):
    def __init__(self, name, duration):
        super().__init__(children=[duration])
        self.name = name
        self.duration = duration
        if name in durations_defintions:
            raise ValueError(f"Duration '{name}' already defined")
        durations_defintions[name] = duration

class DurationTimeNode(DurationASTNode):
    def __init__(self, time_tuple):
        super().__init__(leaf=time_tuple)
        self.time_tuple = time_tuple
        self.duration = (time_tuple[0] * 60 + time_tuple[1]) * 60 + time_tuple[2]
    
    def get_duration(self):
        return self.duration

class DurationDistanceNode(DurationASTNode):
    def __init__(self, distance):
        super().__init__(leaf=distance)
        self.distance_km = distance
        self.distance = int(distance * 1000)
    
    def get_distance(self):
        return self.distance

class DurationCaloriesNode(DurationASTNode):
    def __init__(self, calories):
        super().__init__(leaf=calories)
        self.calories = calories

class DurationHRAboveBelowNode(DurationASTNode):
    def __init__(self, hr_type, hr_value):
        super().__init__(leaf=(hr_type, hr_value))
        self.hr_type = hr_type
        self.hr_value = hr_value

class DurationIDNode(DurationASTNode):
    def __init__(self, name):
        super().__init__(leaf=name)
        self.name = name
        if not name in durations_defintions:
            raise ValueError(f"Duration '{name}' not defined")
        self.duration = durations_defintions[name]
    
    def get_duration(self):
        return self.duration.get_duration()
    
    def get_distance(self):
        return self.duration.get_distance()